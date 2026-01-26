# Peanut Math Worksheets

Generate printable math worksheets (addition/subtraction within 10) in LaTeX/PDF.

## Requirements

- Python 3
- XeLaTeX (`xelatex`)

## Scripts

### Single-page

Generate one worksheet and its answer key.

```bash
python3 generate_worksheet.py --count 20 --date 2025-01-23 --seed 250123
```

Outputs (examples):

- `worksheet_2025-01-23_seed250123.tex`
- `worksheet_2025-01-23_seed250123.pdf`
- `worksheet_2025-01-23_seed250123_ans.tex`
- `worksheet_2025-01-23_seed250123_ans.pdf`

### Multi-page

Generate multiple pages at once. Each page uses its page number as the RNG seed.
The top-right label shows the page number (编号).

```bash
python3 generate_worksheet_multipage.py --start 6 --pages 10 --count 30
```

Outputs (examples):

- `worksheet_no6-pages10-count30.tex`
- `worksheet_no6-pages10-count30.pdf`
- `worksheet_no6-pages10-count30_ans.tex`
- `worksheet_no6-pages10-count30_ans.pdf`

## Notes

- Each page contains `--count` questions.
- The generator avoids duplicate questions and keeps questions with zero below 10%.
- PDF is built by calling `xelatex` internally.
