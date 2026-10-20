---
name: Lehar
description: A portfolio exposure map drawn as a monsoon onset chart; a market move advances from its origin through dated contours to the companies you own.
colors:
  paper: "#F2F5EF"
  paper2: "#E6EDE5"
  paper3: "#DCE6DC"
  card: "#FBFCF9"
  ink: "#0E2D2B"
  ink2: "#3F5C59"
  ink3: "#536A67"
  line: "rgba(14,45,43,.14)"
  line2: "rgba(14,45,43,.26)"
  shell: "#0F3B3A"
  shell2: "#155150"
  onshell: "#F2F5EF"
  onshell2: "rgba(242,245,239,.78)"
  contour: "#1E6F69"
  band1: "#B5DBC6"
  band2: "#CBE6D6"
  band3: "#DEEFE4"
  dry: "#B9C7BF"
  cost: "#B8401C"
  rev: "#1E5E9E"
  rev-ground: "#E8F0F8"
  both: "#6747B0"
  both-ground: "#EFEAF8"
  origin: "#E07A3F"
  on-origin: "#2A1206"
  f1: "#0E2D2B"
  f2: "#2A7F78"
  f3: "#6FB3A9"
  route-sea: "#4E9A91"
  route-mist: "#9CCFC6"
typography:
  display:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "clamp(26px, 2.6vw, 38px)"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "clamp(26px, 2.4vw, 34px)"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  figure:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1.1
    fontVariation: "\"wdth\" 78"
  wordmark:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "26px"
    fontWeight: 700
    letterSpacing: "-0.01em"
    fontVariation: "\"wdth\" 110"
  title:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 650
    lineHeight: 1.2
  body:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "tnum"
  body-small:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.35
    fontFeature: "tnum"
  label:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    letterSpacing: "0.09em"
    fontVariation: "\"wdth\" 78"
  map-region:
    fontFamily: "'Anek Latin', system-ui, sans-serif"
    fontSize: "12.35px"
    fontWeight: 600
    letterSpacing: "0.14em"
    fontVariation: "\"wdth\" 78"
rounded:
  swatch: "2px"
  cell: "4px"
  control: "6px"
  field: "8px"
  menu: "10px"
  card: "12px"
spacing:
  hair: "4px"
  tight: "8px"
  row: "9px"
  gap: "18px"
  panel: "22px"
  gutter: "28px"
  gutter-mobile: "16px"
  column: "36px"
  section: "64px"
components:
  button-primary:
    backgroundColor: "{colors.origin}"
    textColor: "{colors.on-origin}"
    typography: "{typography.title}"
    rounded: "{rounded.field}"
    padding: "10px 16px"
  button-primary-small:
    backgroundColor: "{colors.origin}"
    textColor: "{colors.on-origin}"
    rounded: "{rounded.field}"
    padding: "6px 11px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "6px 11px"
  button-ghost-hover:
    backgroundColor: "{colors.paper2}"
  input:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "9px 11px"
  shell-bar:
    backgroundColor: "{colors.shell}"
    textColor: "{colors.onshell}"
    height: "64px"
    padding: "0 24px"
  nav-link:
    textColor: "{colors.onshell2}"
    rounded: "{rounded.control}"
    padding: "8px 10px"
  nav-link-hover:
    backgroundColor: "{colors.shell2}"
    textColor: "{colors.onshell}"
  side-panel:
    backgroundColor: "{colors.paper2}"
    width: "400px"
    padding: "22px"
  info-card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "14px 16px"
    width: "300px"
  tooltip:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "7px"
    padding: "7px 10px"
---

# Design System: Lehar

## Overview

**Creative North Star: "The Onset Chart"**

Lehar is drawn as a monsoon onset map in the IMD isochrone tradition. A market factor is the origin, pinned bottom-left of the map; teal contours sweep outward from it; industries are wedge-shaped regions fanned around the origin; companies are places sized by the user's money. The page is a working instrument (Operate mode), not a report: the first viewport is the map with a sticky factor panel beside it, and everything below is hairline-ruled sections on the same pale green-grey paper.

Density is high but uncarded. Information sits in ruled rows (1px hairlines at 14% ink) rather than boxed tiles; only floating things (the info card on the map, the search suggestions, the tooltip) lift off the paper. Colour is quarantined: the shell and chrome are monsoon teal and paper, and the saturated hues appear only where they carry data, each paired with a fill pattern so meaning survives greyscale and projection.

One face does all the work. Anek Latin's width axis is the cartographic tool: condensed tracked caps name regions and column heads, the normal width runs the UI, a wide setting is reserved for the wordmark, and tabular figures are on everywhere.

**Key Characteristics:**
- Pale map paper (#F2F5EF) under a deep monsoon-teal shell bar and footer.
- Contours, rainfall-band tints and a radial sweep are the signature; solid contours for measured data, dotted for template-only.
- Data colours (cost orange-red, revenue blue, both-ways violet) each carry a pattern: solid, hatched, cross-hatched.
- Hairline-ruled rows instead of cards; soft shadows only on floating layers.
- One variable face, Anek Latin, with width doing hierarchy work; tabular numerals throughout.

## Colors

A cool green-grey cartographic paper and teal ink, with three IMD-style data hues and one warm origin orange.

### Primary
- **Monsoon Shell Teal** (shell): the sticky top bar, the footer, and the "company estimate" segment of the coverage bar. It is the frame of the instrument. Its lighter step (shell2) is the hover ground for nav links on the bar.
- **Isochrone Teal** (contour): every onset contour, contour labels, the focus ring, the range-slider accent, the selected-factor underline and text, and the solid lines in the "What moved" timeline. It is the line colour of the world.

### Secondary
- **Onset Orange** (origin): the origin pin and its rings on the map, the "today" marker on the timeline, the dot in the logo, and the primary button. Text on it is Burnt Umber (on-origin) for contrast.

### Tertiary (data hues; only on data)
- **Deficit Orange-Red** (cost): a rise in the factor raises the company's costs. Always a solid fill.
- **Excess Blue** (rev): a rise helps revenue. Always hatched at 135 degrees over Rain-Wash Blue (rev-ground). Also the inline link colour.
- **Two-Way Violet** (both): both cost and revenue. Always cross-hatched over Pale Lilac (both-ground).
- **Rainfall Bands** (band1, band2, band3): the reached-zone tints behind the contours, strongest nearest the origin: at least 15% of costs or revenue, 5 to 15%, under 5% or template.
- **Dry Grey-Green** (dry): places a factor does not reach (hollow dots, dry outline), and the unmapped share of the coverage bar.

### Neutral
- **Map Paper** (paper): page ground and the halo stroke behind every map label.
- **Panel Paper** (paper2): the side panel ground, hover rows, ghost-button hover.
- **Track Paper** (paper3): empty factor bars.
- **Survey Card** (card): inputs, the info card, suggestion menu, empty grid cells.
- **Deep Ink / Survey Ink / Faint Ink** (ink, ink2, ink3): primary text, secondary text, captions and region labels.
- **Hairline / Rule** (line, line2): row dividers and region edges; stronger borders on inputs and ghost buttons.

### Fund routes
Holdings are told apart by route. Held directly is Deep Ink (f1); funds take teal steps in order: f2, f3, route-mist, route-sea. The map's place rings split dark (direct) and f3 (through funds).

### Named Rules
**The Quarantine Rule.** Cost, revenue and both-ways hues appear only on data marks (cells, bars, swatches, places). Chrome, headings and buttons never use them. The one exception the build makes is Excess Blue as the link colour.

**The Pattern Twin Rule.** Every data hue ships with its pattern: cost solid, revenue hatched, both cross-hatched, at every size from the 16px swatch to the 30px grid cell. Colour is never the only carrier; the text label says "cost", "revenue" or "both ways" as well.

**The Origin Rule.** Onset Orange marks where a move starts and when the data was run, and the one primary action. Do not spend it on anything else.

## Typography

**Display Font:** Anek Latin (Ek Type), variable width 75 to 125 and weight 300 to 800, with system-ui fallback
**Body Font:** Anek Latin
**Label Font:** Anek Latin at width 78

**Character:** One Indian-made variable face behaving like a survey sheet: condensed caps for the map's place-names, regular width for reading, figures tabular so columns of rupees align.

### Hierarchy
- **Display** (650, clamp 26 to 38px, 1.08): the map headline, one per page, max 24ch.
- **Headline** (650, clamp 26 to 34px, 1.1): section titles below the map.
- **Figure** (700, 26px, width 78): the reach headline ("Crude oil reaches 38% of your money"); the move readout uses the same treatment at 30px; coverage percentages at 20px.
- **Title** (650, 15 to 18px): panel headings, info-card name (17px), sub-section heads (16 to 18px).
- **Body** (400, 16px, 1.5): ledes at 15 to 16px, capped at 52 to 66ch; the callout steps up to 21px at weight 450.
- **Body small** (13.5 to 14.5px): list rows, "what changes" lines, legend; captions and basis notes go to 11.5 to 12.5px in Faint Ink.
- **Label** (600, 12px, 0.09em, uppercase, width 78): table column heads.
- **Map region** (600, about 0.95 of the map font size, 0.14em, uppercase, width 78, Faint Ink, paper halo): industry names on the map.

### Named Rules
**The Width Axis Rule.** Hierarchy on the map comes from width and tracking, not size: condensed tracked caps for regions and column heads, normal width for everything you read, wide (110) only for the Lehar wordmark.

**The Halo Rule.** Every label drawn on the map carries a paper-coloured stroke (4.5 to 5px, painted under the fill) so it reads over contours and bands.

**The Tabular Rule.** Figures are tabular across the whole page; numbers right-align in their column at weight 600 to 650.

## Layout

The first viewport is a two-column stage: the map takes the remaining width and a 400px side panel sits on the right, sticky under the 64px shell bar and scrolling internally. The map is an SVG with a 1000 by 700 viewBox, scaled to fit; its font size is set from the scale so labels stay at least 13px on screen. Below the stage, sections run in a 1240px column with 28px gutters, 64px top padding, separated by full-width hairline rows rather than background changes.

Rows are the unit of density: list rows at 9px vertical padding with a hairline above, table cells at 7 to 9px, legends wrapping in 6 by 18px gaps. Two-column content (what you own, the portfolio editor) uses a fixed 320 to 360px side column and a 36px gap.

Responsive: at 1240px the section nav hides; at 1080px the stage stacks (map at a 10 by 7.4 aspect ratio, panel below, unsticky) and two-column sections become one; at 720px the bar drops to 58px, the portfolio summary moves under the map headline, gutters shrink to 16px, the info card docks to the bottom of the map, and the factor grid becomes a factor picker plus a ruled list.

## Elevation & Depth

Flat paper by default. Depth on the map comes from tonal rainfall bands and the halo strokes, not from shadow. Shadows exist only on layers that float above the paper, and they are soft, teal-tinted and negative-spread so they read as lift rather than outline.

### Shadow Vocabulary
- **Floating card** (`box-shadow: 0 18px 40px -18px rgba(14,45,43,.55), 0 1px 0 rgba(14,45,43,.14)`): the company info card on the map.
- **Menu** (`box-shadow: 0 16px 40px -16px rgba(14,45,43,.5), 0 0 0 1px rgba(14,45,43,.14)`): search suggestions.
- **Button lift** (`box-shadow: 0 6px 16px -8px rgba(14,45,43,.55)` with a 1px rise): primary button hover only.

### Named Rules
**The Paper Rule.** Panels, sections and rows sit flat on paper; if it is not floating over something, it gets no shadow.

## Shapes

Soft but small corners, stepped by role: 2px swatches, 4px grid cells and bar tracks, 6px nav and icon buttons, 8px buttons, inputs and the asset-mix bar, 10px the suggestion menu and empty state, 12px the info card. Places are circles; the origin is a circle with concentric rings. Contours are smooth arcs around the origin, and industry regions are radial wedges bounded by hairlines from it: one geometry carries the contours, the layout and the selection state. Dividers are hairlines, never thick rules, except the mover block, which is bracketed by two stronger rule lines.

## Components

### Buttons
- **Shape:** gently rounded (8px).
- **Primary:** Onset Orange with Burnt Umber text, 650 weight, 15px, padding 10px 16px; small variant 6px 11px at 14px.
- **Hover / Focus:** rises 1px with the button-lift shadow, eased on cubic-bezier(.16,1,.3,1) over 0.2s; focus is a 2px Isochrone Teal outline offset 2px.
- **Ghost:** transparent with a Rule border and ink text; hover fills Panel Paper and drops any shadow.
- **Text actions** ("Show all factors", "Use the latest move"): unstyled buttons with a Rule-coloured underline, Survey Ink to Deep Ink on hover.

### Factor list
The panel's factor picker is a two-column list of ruled rows, not chips: name left, share of your money right, and a 5px bar under each showing the cost, both and revenue split. Hover turns the text Isochrone Teal; the pressed factor is teal, bold, with a 2px teal underline.

### Cards / Containers
- **Corner Style:** 12px on the info card only.
- **Background:** Survey Card.
- **Shadow Strategy:** floating card shadow (see Elevation).
- **Internal Padding:** 14px 16px; rows inside are hairline-ruled.
- Sections and the panel are not cards: they are paper with hairline borders.

### Inputs / Fields
- **Style:** Survey Card ground, 1px Rule border, 8px radius, padding 9px 11px, 15px text.
- **Focus:** 2px Isochrone Teal outline at zero offset, border goes transparent.
- **Error:** message text in Deficit Orange-Red below the field.
- The move slider is a native range with the teal accent, its value shown large in the Figure style.

### Navigation
The shell bar is Monsoon Shell Teal, 64px, sticky: logo mark and wide-axis wordmark left, section links at 15px in 78% paper (hover: full paper on shell2, 6px radius), the portfolio summary right-aligned, then the primary button.

### Onset Map (signature)
Origin pin bottom-left (orange, card-coloured stroke, two faint rings) labelled with the factor and move. Rainfall bands are clipped by a circle that grows from the origin over 1.3s, then three contours draw in over 1s, each labelled along its path. Companies are circles sized by money; reached ones fill with their data pattern, unreached ones are hollow in Dry Grey-Green. Each place has a split ring: dark arc for held directly, f3 arc for through funds. Contours are solid when any company estimate reaches them and dotted (1.5 6) when only industry templates do. Reduced motion removes all transitions.

### Exposure Grid
A separated-border table of 30px cells with 3px gaps: empty cells are Survey Card with a hairline inset, filled cells take the data pattern, and strength is carried by opacity (1, 0.78, 0.55). Column heads run vertically.

### Onset Calendar ("What moved")
An SVG timeline of lanes: each move is a line ending on its as-of date, solid teal 4px for current series, dotted Faint Ink 2px for stale ones, with a dashed orange "data run" line for today.

## Do's and Don'ts

### Do:
- **Do** pair every data hue with its pattern and a text label: cost solid, revenue hatched, both cross-hatched.
- **Do** draw contours solid for measured company data and dotted for template-only reach.
- **Do** put a paper halo stroke under every label drawn on the map.
- **Do** use Anek Latin's width axis for hierarchy: width 78 tracked caps for regions and column heads, width 110 only for the wordmark.
- **Do** separate content with hairlines (rgba(14,45,43,.14)) and keep sections flat on Map Paper.
- **Do** keep figures tabular and right-aligned.

### Don't:
- **Don't** use cost, revenue or both-ways colours on chrome, headings or buttons.
- **Don't** use Onset Orange for anything but the origin, the data-run marker and the single primary action.
- **Don't** box rows into cards; only floating layers (info card, menu, tooltip) lift with a shadow.
- **Don't** use shell2 (#155150) or any colour close to Deep Ink as a fund-route colour; routes must stay distinguishable from direct holdings.
- **Don't** let a contour label sit on top of a place label; place names take priority.

## Known gaps (shipped, not part of the system)

The final review disposition was "fix"; the user chose to ship with these open:
- Contour labels can overprint place labels on the map.
- The third fund-route colour in the build is #155150 (shell2), too close to the direct-holding ink (f1); the rule above is the intended fix.
- The "What moved" timeline is unreadable under 720px wide.

Drift in the build, not canonized: tokens --f4, --f5 and --f6 are declared but unused; fund-route and asset-mix colours (#4E9A91, #9CCFC6, #7E918C, #A9B8B2) are hard-coded in the script rather than read from tokens.

Where the build departs from the direction contract: the portfolio editor is an in-page section reached from the primary button, not a drawer; industries are radial wedges around the origin rather than geographic-style regions; and Onset Orange, not specified in the contract, is the primary button colour as well as the origin.
