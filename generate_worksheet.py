#!/usr/bin/env python3
import argparse
import datetime as dt
import random
import re
import subprocess
from pathlib import Path


ARRAY_STRETCH = "1.1"
ROW_GAP = "0.6em"
GEOMETRY = "left=0.4in,right=0.7in,top=0.5in,bottom=0.5in"


def sanitize_filename(text):
    slug = re.sub(r"[^0-9A-Za-z]+", "-", text).strip("-")
    return slug or "date"


def build_question(rng):
    op = rng.choice(["+", "-"])
    if op == "+":
        a = rng.randint(0, 10)
        b = rng.randint(0, 10 - a)
        c = a + b
    else:
        a = rng.randint(0, 10)
        b = rng.randint(0, a)
        c = a - b

    blank = rng.choice(["a", "b", "c"])
    key = f"{a}{op}{b}={c}"
    has_zero = (a == 0) or (b == 0) or (c == 0)

    if blank == "a":
        lhs_q = f"\\blank{op}{b}"
        rhs_q = str(c)
        lhs_a = f"\\ans{{{a}}}{op}{b}"
        rhs_a = str(c)
    elif blank == "b":
        lhs_q = f"{a}{op}\\blank"
        rhs_q = str(c)
        lhs_a = f"{a}{op}\\ans{{{b}}}"
        rhs_a = str(c)
    else:
        lhs_q = f"{a}{op}{b}"
        rhs_q = "\\blank"
        lhs_a = f"{a}{op}{b}"
        rhs_a = f"\\ans{{{c}}}"

    return lhs_q, rhs_q, lhs_a, rhs_a, key, has_zero


def chunked(items, n):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def build_rows(questions, use_answers):
    rows = []
    row_list = list(chunked(questions, 3))
    for row_index, row in enumerate(row_list):
        cells = []
        for q in row:
            lhs = q["lhs_a"] if use_answers else q["lhs_q"]
            rhs = q["rhs_a"] if use_answers else q["rhs_q"]
            cells.extend(
                [
                    f"\\qnum{{{q['num']}}}",
                    f"\\lhs{{{lhs}}}",
                    f"\\rhs{{{rhs}}}",
                ]
            )
        missing = 3 - len(row)
        for _ in range(missing):
            cells.append("\\multicolumn{3}{@{}l@{}}{}")

        line = " & ".join(cells)
        if row_index < len(row_list) - 1:
            line += rf" \\[{ROW_GAP}]"
        else:
            line += r" \\"
        rows.append(line)
    return "\n".join(rows)


def render_tex(rows, date_str, total, is_answer):
    title = "答案" if is_answer else "十以内加减法练习"
    lines = [
        r"\documentclass[12pt]{article}",
        r"\usepackage[UTF8,fontset=fandol]{ctex}",
        rf"\usepackage[{GEOMETRY}]{{geometry}}",
        r"\usepackage{array}",
        r"\usepackage{amsmath}",
        r"\usepackage{xcolor}",
        r"",
        r"\newcommand{\blank}{\underline{\makebox[0.6cm]{}}}",
    ]
    if is_answer:
        lines.append(
            r"\newcommand{\ans}[1]{\underline{\makebox[0.6cm][c]{\textcolor{red}{\textbf{#1}}}}}"
        )
    lines.extend(
        [
            r"\newcommand{\scoreblank}{\underline{\makebox[1.6cm]{}}}",
            r"\newcommand{\qnum}[1]{\textcolor{blue}{\zihao{5}\ttfamily(#1)}}",
            r"\newcommand{\lhs}[1]{\mbox{$#1$}}",
            r"\newcommand{\rhs}[1]{\mbox{$#1$}}",
            r"\newcolumntype{Q}{>{\raggedleft\arraybackslash}p{2.0em}}",
            r"",
            r"\begin{document}",
            r"\pagestyle{empty}",
            r"",
            r"\begin{flushright}",
            f"{{\\zihao{{4}} 日期：{date_str}\\\\",
            f"正确数：\\scoreblank/{total}}}",
            r"\end{flushright}",
            r"",
            r"\begin{center}",
            f"{{\\zihao{{1}}\\textbf{{{title}}}}}\\\\[0.5em]",
            r"\end{center}",
            r"",
            r"\zihao{2}",
            r"\setlength{\tabcolsep}{0pt}",
            rf"\renewcommand{{\arraystretch}}{{{ARRAY_STRETCH}}}",
            r"",
            r"\begin{tabular}{@{}Q@{\hspace{0.6em}}r@{$=$}l@{\hspace{0.8em}}Q@{\hspace{0.6em}}r@{$=$}l@{\hspace{0.8em}}Q@{\hspace{0.6em}}r@{$=$}l@{}}",
            rows,
            r"\end{tabular}",
            r"",
            r"\end{document}",
            r"",
        ]
    )
    return "\n".join(lines)


def run_xelatex(tex_path):
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", tex_path.name],
        cwd=tex_path.parent,
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate a math worksheet PDF.")
    parser.add_argument("--count", type=int, default=20, help="Number of questions.")
    parser.add_argument("--seed", type=int, help="Random seed.")
    parser.add_argument("--date", type=str, help="Date string shown on the worksheet.")
    args = parser.parse_args()

    if args.count <= 0:
        raise SystemExit("count must be positive")

    date_str = args.date or dt.date.today().strftime("%Y-%m-%d")
    seed = args.seed if args.seed is not None else int(dt.datetime.now().timestamp())
    rng = random.Random(seed)

    # Keep zero problems strictly under 10% of the total.
    zero_limit = max(0, (args.count - 1) // 10)
    questions = []
    seen = set()
    zero_count = 0
    attempts = 0
    max_attempts = args.count * 200
    while len(questions) < args.count and attempts < max_attempts:
        attempts += 1
        lhs_q, rhs_q, lhs_a, rhs_a, key, has_zero = build_question(rng)
        if key in seen:
            continue
        if has_zero and zero_count >= zero_limit:
            continue
        seen.add(key)
        if has_zero:
            zero_count += 1
        questions.append(
            {
                "num": len(questions) + 1,
                "lhs_q": lhs_q,
                "rhs_q": rhs_q,
                "lhs_a": lhs_a,
                "rhs_a": rhs_a,
            }
        )

    if len(questions) < args.count:
        raise SystemExit(
            "unable to generate enough unique questions; reduce --count or adjust rules"
        )

    rows_q = build_rows(questions, use_answers=False)
    rows_a = build_rows(questions, use_answers=True)

    base_date = sanitize_filename(date_str)
    base = f"{base_date}_seed{seed}"

    out_dir = Path.cwd()
    tex_q = out_dir / f"worksheet_{base}.tex"
    tex_a = out_dir / f"worksheet_{base}_ans.tex"

    tex_q.write_text(render_tex(rows_q, date_str, args.count, is_answer=False), encoding="utf-8")
    tex_a.write_text(render_tex(rows_a, date_str, args.count, is_answer=True), encoding="utf-8")

    run_xelatex(tex_q)
    run_xelatex(tex_a)

    print(f"Generated: {tex_q.name}, {tex_a.name}")


if __name__ == "__main__":
    main()
