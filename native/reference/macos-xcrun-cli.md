# Terminal / CI Command Reference — Mac Apps

Production command reference for building, signing, notarizing, packaging, and debugging macOS apps from the terminal or CI. Owns exact flag syntax; `reference/distribution.md` owns the decision/flow narrative and cross-references back here for command detail — do not duplicate the flow explanation in both files.

> Scope: `xcodebuild`, `xcresulttool`, `codesign`, `security`, `notarytool`, `stapler`, `spctl`, `pkgbuild`/`productbuild`/`productsign`, `hdiutil`, `otool`/`install_name_tool`, `atos`, `log`, `defaults`, and a CI recipe.

---

## 1. `xcodebuild` — Build / Archive / Export

| Command | Purpose |
|---|---|
| `xcodebuild -list -project App.xcodeproj` | Enumerate schemes/targets/configurations |
| `xcodebuild -showBuildSettings -scheme App` | Dump resolved build settings (verify signing identity, bundle ID, deployment target) |
| `xcodebuild build -scheme App -destination 'platform=macOS' -configuration Release` | Build for the local Mac |
| `xcodebuild build -scheme App -destination 'platform=macOS,arch=arm64' -configuration Release` | Pin to a single architecture (debugging arch-specific issues) |
| `xcodebuild test -scheme AppTests -destination 'platform=macOS' -resultBundlePath TestResults.xcresult -enableCodeCoverage YES` | Run tests, machine-readable result bundle |
| `xcodebuild archive -scheme App -configuration Release -archivePath build/App.xcarchive` | Produce an `.xcarchive` |
| `xcodebuild -exportArchive -archivePath build/App.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/export` | Export a distributable `.app`/`.pkg` from the archive per the export method |

### 1.1 `ExportOptions.plist` Variants

| `method` value | Use |
|---|---|
| `developer-id` | Developer ID direct distribution — exports a signed `.app` ready for zip/DMG + notarization |
| `mac-application` | Ad-hoc/local export for Mac App Store-signed builds intended for internal testing, not submission |
| `app-store-connect` (or `app-store`, verify against the Xcode version's schema) | Produces the `.pkg` suitable for App Store Connect upload |

```xml
<!-- ExportOptions-developer-id.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>method</key>
    <string>developer-id</string>
    <key>teamID</key>
    <string>TEAMID1234</string>
    <key>signingStyle</key>
    <string>manual</string>
    <key>signingCertificate</key>
    <string>Developer ID Application</string>
</dict>
</plist>
```

**Export-method strings.** `app-store-connect` is the current value for App Store submission; `app-store` is its deprecated predecessor and still accepted by older Xcode. `developer-id` (direct distribution, notarized) and `mac-application` (unsigned/local) are the other Mac-relevant values. Pin the string to your CI's Xcode version — `xcodebuild -help` lists what that toolchain accepts.

---

## 2. `xcresulttool` — Result Bundle Parsing

| Command | Purpose |
|---|---|
| `xcrun xcresulttool get --path TestResults.xcresult --format json` | Top-level test summary as JSON |
| `xcrun xcresulttool get --path TestResults.xcresult --id <ref> --format json` | Follow a nested reference (per-test detail, attachments) |
| `xcrun xcresulttool get --path TestResults.xcresult --id <attachmentRef> > failure.png` | Extract a failure screenshot/attachment |
| `xcrun xcresulttool get --legacy --path TestResults.xcresult --format json` | Force the pre-Xcode-16 schema shape if a downstream parser hasn't migrated |

> Xcode 16 changed the result-bundle schema (new structure under `actions._values`) — pin a parser to the Xcode version in CI or use `--legacy`.

---

## 3. `codesign`

| Command | Purpose | Gotcha |
|---|---|---|
| `codesign -s "Developer ID Application: Example Inc (TEAMID1234)" --options runtime --entitlements App.entitlements App.app` | Sign with hardened runtime + entitlements | Identity string must match `security find-identity` output exactly, including the parenthesized Team ID |
| `codesign -s "Developer ID Application: Example Inc" --options runtime App.app/Contents/XPCServices/Helper.xpc` | Sign an embedded XPC service | Sign inside-out — see `reference/distribution.md` § 4 for full ordering |
| `codesign --deep -s "Developer ID Application: Example Inc" App.app` | One-pass signing of the whole bundle tree | Applies **one entitlements file to every embedded component** — wrong whenever an XPC service needs narrower entitlements than the host app; prefer manual per-component signing (§ above) for anything nontrivial |
| `codesign -dv --verbose=4 App.app` | Verbose signing inspection (identity, Team ID, sealed resources) | Use before notarization submission to catch identity mismatches early |
| `codesign --display --entitlements - App.app` | Print the entitlements actually embedded in the signed binary | The ground truth for "what did I actually ship" — compare against the source `.entitlements` file |
| `codesign --verify --deep --strict --verbose=2 App.app` | Verify the full signature chain including nested code | Run after signing, before packaging — catches deep-signing order mistakes |

---

## 4. `security` — Keychain for CI

| Command | Purpose |
|---|---|
| `security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain` | Create an ephemeral CI keychain |
| `security default-keychain -s build.keychain` | Make it the default so `codesign` finds it without `--keychain` on every call |
| `security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain` | Unlock (required before import/use) |
| `security import DeveloperIDApplication.p12 -k build.keychain -P "$P12_PASSWORD" -T /usr/bin/codesign` | Import the signing certificate + private key |
| `security set-key-partition-list -S apple-tool:,apple: -s -k "$KEYCHAIN_PASSWORD" build.keychain` | Grant `codesign`/`security` non-interactive access to the imported key (required on modern macOS or signing hangs on a GUI prompt that doesn't exist in CI) |
| `security find-identity -p codesigning -v build.keychain` | List usable signing identities — confirms the import succeeded with the right usage flags |
| `security delete-keychain build.keychain` | Teardown at end of CI job |

---

## 5. `notarytool` — Submission and History

| Command | Purpose |
|---|---|
| `xcrun notarytool store-credentials "AC_PROFILE" --apple-id you@example.com --team-id TEAMID1234 --password <app-specific-password>` | One-time: save credentials to the local keychain under a named profile |
| `xcrun notarytool submit App.zip --keychain-profile "AC_PROFILE" --wait` | Submit + block until Apple's notary service finishes processing |
| `xcrun notarytool submit App.dmg --keychain-profile "AC_PROFILE" --wait` | Same, for a DMG (DMG/PKG/ZIP of a signed `.app` are all valid submission artifacts) |
| `xcrun notarytool history --keychain-profile "AC_PROFILE"` | List recent submissions |
| `xcrun notarytool info <submission-id> --keychain-profile "AC_PROFILE"` | Poll status of a specific submission without blocking (alternative to `--wait`) |
| `xcrun notarytool log <submission-id> --keychain-profile "AC_PROFILE"` | Fetch the detailed issue log for a rejected (or accepted-with-warnings) submission |

- App-specific password: generate at appleid.apple.com, not the account's primary password.
- `--keychain-profile` is the CI-friendly alternative to passing `--apple-id`/`--team-id`/`--password` inline on every call — set it up once via `store-credentials` in a keychain accessible to the CI runner (same `build.keychain` from § 4 works).

---

## 6. `stapler` / `spctl`

| Command | Purpose |
|---|---|
| `xcrun stapler staple App.app` | Attach the notarization ticket to the `.app` bundle |
| `xcrun stapler staple App.dmg` | Attach the ticket to the DMG container itself (recommended for the artifact actually distributed — see `reference/distribution.md` § 5) |
| `xcrun stapler validate App.app` | Verify a ticket is stapled without re-submitting |
| `spctl -a -vvv App.app` | Assess Gatekeeper acceptance of the app (`-a` assess, `-vvv` verbose) |
| `spctl -a -vvv -t install App.pkg` | Assess a `.pkg` installer specifically (`-t install` type) |
| `spctl --assess --type execute App.app` | Explicit long-form equivalent of `-a` for an executable bundle |

Expected success output includes `source=Notarized Developer ID` — anything else (`source=Unnotarized Developer ID`, `rejected`) means either notarization wasn't submitted, wasn't stapled, or the artifact was modified after signing.

---

## 7. `pkgbuild` / `productbuild` / `productsign`

| Command | Purpose |
|---|---|
| `pkgbuild --root ./payload --identifier com.example.myapp.pkg --version 1.2.0 --install-location /Applications --scripts ./scripts ComponentApp.pkg` | Build a single-component installer package from a payload directory |
| `pkgbuild --component App.app --install-location /Applications AppComponent.pkg` | Component package directly from an `.app` bundle |
| `productbuild --synthesize --package AppComponent.pkg distribution.xml` | Generate a starter distribution XML from one or more component packages |
| `productbuild --distribution distribution.xml --package-path . --resources ./Resources Final.pkg` | Compose the final distribution package (multi-component, welcome/license/conclusion panes) |
| `productsign --sign "Developer ID Installer: Example Inc (TEAMID1234)" Final.pkg Final-signed.pkg` | Sign the installer package with the **Installer** certificate (distinct from the Application certificate used for the `.app` itself) |
| `pkgutil --check-signature Final-signed.pkg` | Verify the package's signature chain |

---

## 8. `hdiutil` — DMG Creation

| Command | Purpose |
|---|---|
| `hdiutil create -volname "My App" -srcfolder ./staging -ov -format UDZO App.dmg` | Compressed DMG from a staged folder (app + Applications symlink) |
| `hdiutil create -size 200m -fs HFS+ -volname "My App" App-rw.dmg` | Empty, writable DMG for scripted population before compressing |
| `hdiutil attach App-rw.dmg` | Mount for scripted asset copying (background image, `.DS_Store` layout) |
| `hdiutil detach /Volumes/My\ App` | Unmount after populating |
| `hdiutil convert App-rw.dmg -format UDZO -o App-final.dmg` | Convert a writable working DMG to the final compressed read-only distributable |

Community wrapper `create-dmg` scripts this whole sequence (icon positions, background image, window size) — evaluate as a build dependency rather than reimplementing the `hdiutil` choreography by hand unless the CI environment can't install it.

---

## 9. `otool` / `install_name_tool` — Embedded Framework Paths

| Command | Purpose |
|---|---|
| `otool -L App.app/Contents/MacOS/App` | List linked dynamic libraries and their install-name paths |
| `otool -l App.app/Contents/MacOS/App \| grep -A2 LC_RPATH` | Inspect `@rpath` search paths baked into the binary |
| `install_name_tool -change /old/path/to/lib.dylib @rpath/lib.dylib App.app/Contents/MacOS/App` | Repoint a linked library's install name (fixing a mis-linked embedded framework) |
| `install_name_tool -add_rpath @executable_path/../Frameworks App.app/Contents/MacOS/App` | Add an `@rpath` entry so embedded `Frameworks/` resolves at runtime |

Re-sign the binary after any `install_name_tool` mutation — changing load commands invalidates the existing signature.

---

## 10. `atos` / Symbolication

| Command | Purpose |
|---|---|
| `dwarfdump --uuid App.app.dSYM` | Print the dSYM's UUID — must match the crashed binary's UUID before symbolication is trustworthy |
| `atos -o App.app.dSYM/Contents/Resources/DWARF/App -arch arm64 -l <loadAddress> <crashAddress>` | Symbolicate a single address from a crash report |
| `xcrun symbolicatecrash CrashReport.crash App.app.dSYM > Symbolicated.crash` | Symbolicate a full `.crash` report (may require `DEVELOPER_DIR` set explicitly; tool location has moved across Xcode versions) |

A UUID mismatch between the dSYM and the binary produces plausible-looking but wrong symbol names — always verify with `dwarfdump --uuid` before trusting output.

---

## 11. `log` / `log stream` — Running App

| Command | Purpose |
|---|---|
| `log stream --predicate 'subsystem == "com.example.myapp"'` | Live-stream unified log entries from the app's OSLog subsystem |
| `log stream --predicate 'process == "App"'` | Stream by process name instead of subsystem |
| `log show --predicate 'subsystem == "com.example.myapp"' --last 1h` | Retrospective query over the last hour |
| `log stream --predicate 'subsystem == "com.example.myapp.HelperService"'` | Debugging an embedded XPC service specifically — see `reference/xpc-helpers.md` § 7 |

---

## 12. `defaults` — Reading App Prefs During Debugging

| Command | Purpose |
|---|---|
| `defaults read com.example.myapp` | Dump the app's preference domain |
| `defaults read com.example.myapp SomeKey` | Read a single key |
| `defaults write com.example.myapp SomeKey -bool YES` | Force a preference value for testing |
| `defaults read group.com.example.myapp` | Read an App-Group-scoped shared preferences domain (`reference/sandbox-entitlements.md` § 7) |

Sandboxed apps store preferences inside the app's container (`~/Library/Containers/com.example.myapp/Data/Library/Preferences/`) — `defaults read <bundle-id>` still resolves correctly against the container path, but direct `plutil`/`cat` access needs the full container path if bypassing `defaults`.

---

## 13. CI Recipe — GitHub Actions macOS Runner

```yaml
name: build-sign-notarize
on: [workflow_dispatch]

jobs:
  release:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4

      - name: Import signing certificate
        env:
          P12_BASE64: ${{ secrets.DEVELOPER_ID_P12_BASE64 }}
          P12_PASSWORD: ${{ secrets.DEVELOPER_ID_P12_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.CI_KEYCHAIN_PASSWORD }}
        run: |
          echo "$P12_BASE64" | base64 --decode > cert.p12
          security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security import cert.p12 -k build.keychain -P "$P12_PASSWORD" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple: -s -k "$KEYCHAIN_PASSWORD" build.keychain
          rm cert.p12

      - name: Build and archive
        run: |
          xcodebuild archive -scheme App -configuration Release \
            -archivePath build/App.xcarchive

      - name: Export signed app
        run: |
          xcodebuild -exportArchive -archivePath build/App.xcarchive \
            -exportOptionsPlist ExportOptions-developer-id.plist \
            -exportPath build/export

      - name: Verify signature
        run: codesign -dv --verbose=4 build/export/App.app

      - name: Package DMG
        run: |
          mkdir -p staging
          cp -R build/export/App.app staging/
          ln -s /Applications staging/Applications
          hdiutil create -volname "App" -srcfolder staging -ov -format UDZO build/App.dmg

      - name: Notarize
        env:
          AC_PROFILE_CREDS: ${{ secrets.NOTARYTOOL_KEYCHAIN_PROFILE_SETUP }}
        run: |
          xcrun notarytool store-credentials "AC_PROFILE" \
            --apple-id "${{ secrets.APPLE_ID }}" \
            --team-id "${{ secrets.TEAM_ID }}" \
            --password "${{ secrets.APP_SPECIFIC_PASSWORD }}"
          xcrun notarytool submit build/App.dmg --keychain-profile "AC_PROFILE" --wait

      - name: Staple
        run: xcrun stapler staple build/App.dmg

      - name: Verify Gatekeeper acceptance
        run: spctl -a -vvv -t install build/App.dmg || spctl -a -vvv build/App.dmg

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: App.dmg
          path: build/App.dmg

      - name: Clean up keychain
        if: always()
        run: security delete-keychain build.keychain
```

---

## 14. Gotchas

1. **`xcodebuild` export method strings drift across Xcode versions** — confirm `ExportOptions.plist` `method` values against `xcodebuild -help` for the pinned Xcode before hardcoding in CI (§ 1.1).
2. **`codesign --deep` applies one entitlements file to the whole tree** — wrong for any bundle with an XPC service needing narrower entitlements than the host app; sign inside-out manually instead (§ 3, full order in `reference/distribution.md` § 4).
3. **`set-key-partition-list` is required on CI keychains** — without it, `codesign`/`notarytool` hang waiting for a GUI keychain-access prompt that doesn't exist on a headless runner.
4. **Staple the artifact you actually ship** — stapling only the inner `.app` before zipping/DMG-wrapping still works for Gatekeeper's on-open check, but stapling the outer `.dmg`/`.pkg` additionally allows offline validation before the user opens it (`reference/distribution.md` § 5).
5. **`atos`/`symbolicatecrash` need a matching dSYM UUID** — `dwarfdump --uuid` on the dSYM must equal the crash report's binary UUID, or output is silently wrong, not an error.
6. **`install_name_tool` invalidates the existing signature** — always re-sign after mutating load commands.
7. **`xcresulttool`'s Xcode 16 schema break** — pin parsers to the CI Xcode version or use `--legacy`.
8. **App-specific password, not account password** — `notarytool`/`store-credentials` require a per-app password generated at appleid.apple.com; the account's primary password will not authenticate.

---

## Sources

- [Distributing command-line tools outside the Mac App Store / Notarizing macOS software | Apple Developer Documentation](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) (accessed 2026-07)
- [NOTARYTOOL(1) man page](https://keith.github.io/xcode-man-pages/notarytool.1.html) (accessed 2026-07)
- [Xcode Help — xcodebuild reference](https://developer.apple.com/documentation/xcode)
- [codesign man page — Apple Developer / macOS manpages](https://developer.apple.com/library/archive/technotes/tn2206/_index.html) (Code Signing In Depth, cross-reference against current `man codesign` on the CI runner's macOS version)
- [Packaging and distributing software (pkgbuild/productbuild) | Apple Developer Documentation](https://developer.apple.com/documentation/xcode/packaging-and-distributing-software-for-manual-installation)
- Cross-reference: `reference/distribution.md` (channel decision, signing-order narrative, Sparkle/App-Store flow), `reference/sandbox-entitlements.md` (entitlement catalog `codesign --entitlements` inspects), `reference/xpc-helpers.md` (§ 7 debugging commands for embedded XPC services), `reference/xcrun-cli.md` (iOS/simulator counterpart — `simctl`/`devicectl`)
