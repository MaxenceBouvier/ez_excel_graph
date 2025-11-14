# Resources Directory

This directory is for your Excel data files.

## ⚠️ IMPORTANT - DATA PRIVACY ⚠️

**NEVER commit your actual Excel data files to GitHub!**

All Excel files (`.xlsx`, `.xls`, `.xlsm`, `.csv`) in this directory are automatically ignored by git and **WILL NOT** be pushed to GitHub. This protects your private data.

### What gets committed:
- ✅ `example_template.xlsx` - Empty template showing the expected data format
- ✅ This README file

### What does NOT get committed:
- ❌ Any other Excel files with your actual data
- ❌ CSV files
- ❌ Any files containing real speaking data

### Multiple layers of protection:

1. **`.gitignore`**: All Excel files are blocked (except the template)
2. **Pre-commit hook**: Automatically prevents committing Excel data files
3. **This warning**: Reminds you to keep data local

## Expected Data Format

Your Excel files should have sheets with the following column structure:

| speak_time | speak_person | idea_1 | idea_2 | idea_3 | ... |
|------------|--------------|--------|--------|--------|-----|
| T1 or 1    | P1 or Name   | value  | value  | value  | ... |
| T1 or 1    | P1 or Name   | value  | value  | value  | ... |
| T2 or 2    | P2 or Name   | value  | value  | value  | ... |
| ...        | ...          | ...    | ...    | ...    | ... |

### Column descriptions:

- **speak_time**: The round/time period when someone spoke (T1, T2, T3... or 1, 2, 3...)
- **speak_person**: The person who spoke (P1, P2, P3... or actual names)
- **idea_X**: Multiple columns for different ideas/topics (can contain repeated values)

### Example:

```
T1, P1, Innovation, Collaboration, Innovation
T1, P1, Technology, Innovation, Design
T2, P5, Collaboration, Strategy, Technology
T18, P1, Design, Innovation, Technology
```

## Using Your Data

1. **Place your Excel files here** in the `resources/` directory
2. **They stay on your computer** - never uploaded to GitHub
3. **Use Claude Code** to generate graphs:
   ```bash
   claude
   > "Generate a timeline chart from my Excel data in resources/"
   ```

## Template File

The `example_template.xlsx` file is an empty template showing the column structure. You can:
- Use it as a starting point
- Copy it and fill in your data
- Or create your own Excel file with the same column structure

## Questions?

If you have questions about the data format or privacy, ask Claude Code:
```bash
claude
> "How do I structure my Excel data?"
> "Confirm that my Excel files won't be uploaded to GitHub"
```
