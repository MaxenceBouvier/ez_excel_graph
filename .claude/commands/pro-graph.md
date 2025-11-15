---
description: Create a publication-ready, professional graph from user's Excel data with proper axis labels, legends, titles, and styling
---

You are helping a social science researcher create a **publication-ready graph** for their academic paper.

## Your Task

1. **Understand the data**: Ask the user what they want to visualize if not already clear
2. **Choose the right visualization**: Recommend the most appropriate chart type (scatter, line, bar, heatmap, box plot, etc.)
3. **Create a professional graph** following ALL these requirements:

### MANDATORY Requirements

**Axis Labels:**
- X-axis: Descriptive label with units (e.g., "Participant Age (years)")
- Y-axis: Descriptive label with units (e.g., "Response Time (seconds)")

**Colorbar (if applicable):**
- Label the colorbar with what it represents (e.g., "Frequency", "Correlation Coefficient")

**Legend:**
- Include meaningful legend labels (e.g., "Control Group", "Treatment Group")
- Position legend to not obscure data

**Title & Caption:**
- Suggest 2-3 publication-ready titles for the user to choose from
- Provide a draft figure caption suitable for a research paper
- Ask if they need the title adjusted for their specific research context

**Styling:**
- Use 300 DPI for static images (PNG/PDF)
- Set figure size to 8x6 inches minimum
- Use readable font sizes (12pt for labels, 14pt for titles)
- Apply professional color schemes (consider colorblind-friendly palettes)
- Add subtle grid lines for readability
- Use `tight_layout()` to prevent label cutoff

### Workflow

1. **Data Inspection**: Examine the CSV data to understand column names and data types
2. **Recommendation**: Suggest the best visualization type and explain why
3. **Create Graph**: Generate the professional graph following all requirements above
4. **Suggest Titles**: Provide 2-3 alternative titles for user selection
5. **Draft Caption**: Write a publication-ready figure caption (1-2 sentences describing what's shown)
6. **Save**: Output to appropriate project folder (outputs/PROJECT/png/ or outputs/PROJECT/pdf/)
7. **Offer Refinements**: Ask if they want to adjust colors, add annotations, or modify the style

### Example Interaction

"I've created a scatter plot showing the relationship between participant age and response time. Here are three title options:

1. 'Response Time by Participant Age'
2. 'Age-Related Differences in Response Time'
3. 'Participant Response Time Across Age Groups'

**Suggested caption:**
'Figure 1. Scatter plot showing the relationship between participant age and response time (n=45). Each point represents one participant. Pearson correlation r=0.67, p<0.001.'

Would you like me to adjust the title, modify the styling, or add any annotations?"

### Technical Checklist

Before saving, verify:
- ✓ X and Y axes have descriptive labels with units
- ✓ Colorbar labeled (if present)
- ✓ Legend included with clear labels (if multiple series)
- ✓ Title suggested to user
- ✓ Figure caption drafted
- ✓ DPI = 300 (for PNG/PDF)
- ✓ Font sizes readable (min 12pt)
- ✓ No overlapping text
- ✓ Grid lines present (if they help readability)
- ✓ Tight layout applied

Now proceed to help the user create their professional graph!
