# Peanut Math Worksheets

Generate printable math worksheets (addition/subtraction within 10) in LaTeX/PDF.

codex resume 019bf57e-90b5-7021-88d3-6bfef89c2a32

## Requirements

- Python 3
- XeLaTeX (`xelatex`)

## Directory

All scripts and generated files for the within-10 addition/subtraction worksheets
are in `within_10_add_sub/`. Run the scripts from that directory so outputs are
written there.

## Scripts

### Single-page

Generate one worksheet and its answer key.

```bash
cd within_10_add_sub
python3 generate_worksheet.py --count 20 --date 2025-01-23 --seed 250123
```

Outputs (examples):

- `within_10_add_sub/worksheet_2025-01-23_seed250123.tex`
- `within_10_add_sub/worksheet_2025-01-23_seed250123.pdf`
- `within_10_add_sub/worksheet_2025-01-23_seed250123_ans.tex`
- `within_10_add_sub/worksheet_2025-01-23_seed250123_ans.pdf`

### Multi-page

Generate multiple pages at once. Each page uses its page number as the RNG seed.
The top-right label shows the page number (编号).

```bash
cd within_10_add_sub
python3 generate_worksheet_multipage.py --start 6 --pages 10 --count 30
```

Outputs (examples):

- `within_10_add_sub/worksheet_no6-pages10-count30.tex`
- `within_10_add_sub/worksheet_no6-pages10-count30.pdf`
- `within_10_add_sub/worksheet_no6-pages10-count30_ans.tex`
- `within_10_add_sub/worksheet_no6-pages10-count30_ans.pdf`

## Notes

- Each page contains `--count` questions.
- The generator avoids duplicate questions and keeps questions with zero below 10%.
- PDF is built by calling `xelatex` internally.
