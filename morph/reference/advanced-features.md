# Advanced Features Guide

Purpose: Use this reference when the task includes archival, signatures, watermarks, PDF manipulation, encryption, metadata control, or compression.

## Contents

- PDF/A
- Digital signatures
- Watermarks
- Merge and split
- Bookmarks and TOC
- Page manipulation
- Encryption and metadata
- Compression

## PDF/A

| Variant | Best fit |
|--------|----------|
| PDF/A-1b | Text-heavy docs |
| PDF/A-2b | Japanese docs and transparency-safe archival |
| PDF/A-2a | Accessibility + archival |
| PDF/A-3b | Archival with attachments |

```sh
# Create PDF then convert to PDF/A-2b
pandoc input.md -o temp.pdf --pdf-engine=xelatex
gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=output-pdfa.pdf temp.pdf
verapdf --flavour 2b output-pdfa.pdf
```

## Digital Signatures

Rules:

- Ask first for signing requirements.
- Prefer dedicated signing tools.
- `pdfsig` is primarily for verification.

```sh
pdfsig input.pdf
pdfsig -v signed.pdf
```

## Watermarks

```sh
pdftk input.pdf stamp watermark.pdf output output-watermarked.pdf
```

Use watermarking for explicit draft or distribution control only when requested or policy-backed.

## Merge And Split

```sh
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf
pdfunite file1.pdf file2.pdf merged.pdf

# Split
pdftk input.pdf burst output page_%02d.pdf
pdfseparate input.pdf page_%d.pdf
```

## Bookmarks And TOC

```sh
# TOC via Pandoc
pandoc input.md -o output.pdf --pdf-engine=xelatex --toc

# Inject bookmark info
pdftk input.pdf update_info bookmarks.txt output output-with-bookmarks.pdf
```

## Page Manipulation

```sh
# Rotate
pdftk input.pdf rotate 1-endright output rotated.pdf

# Reorder
pdftk input.pdf cat 3 1 2 5 4 output reordered.pdf

# Resize to A4
gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=a4-output.pdf input.pdf
```

## Encryption And Metadata

```sh
# Password protection
pdftk input.pdf output protected.pdf owner_pw "owner_password" user_pw "user_password"

# 256-bit AES encryption
qpdf --encrypt "user_pw" "owner_pw" 256 -- input.pdf encrypted.pdf

# Metadata
pdfinfo input.pdf
pdftk input.pdf dump_data
exiftool input.pdf
```

Rules:

- Ask first for encryption, password, or signature workflows.
- Do not invent security settings or passwords.

## Compression

```sh
# Compress
gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=compressed.pdf input.pdf

# Linearize
qpdf --linearize input.pdf linearized.pdf
```
