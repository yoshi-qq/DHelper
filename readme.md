# DHelper – card generator for DnD 5e

## Welcome

This is DHelper, a python-based Dungeons and Dragons 5th edition item, weapon, armor and spell card generator. This project ist far from done but I hope it can help someone in my exact situation.

## Overview

DHelper started as a small private project and aims to make managing custom game cards easy. It is now open to the community for contributions. Players, game masters and homebrew designers can generate printable cards based on their needs.

## Features

### Current

- **Spell Cards** with fields such as name, level, casting time and components
- **Item & Weapon Cards** including damage dice, attributes and ranges
- **Armor Cards** for shields and protection
- **Multi-language** support (currently English and German)

### Planned

- **Monster Cards**
- **Enchantments** for items (a custom feature similar to item enchants in games like Minecraft)
- **UI Overhaul**
- **Exports** to PDF/PNG sheets and print templates
- **Distributable Executable**
- **Detailed Guide**

## Installation

1. Install Python 3.13.x
2. Clone this repository or download the ZIP
3. Install dependencies (pillow)

   ```bash
   pip install pillow
   ```

4. Run the program

   ```bash
   python src/main.py
   ```

## Usage

Launching the program shows the main menu. Choose "New Spell" or "New Item" in the appropriate menu and fill out the form. Save to generate the card image. Existing entries can be managed and printed from the respective menus.

## Card Types

- **Spell Cards** – ID, Name, Level, Range, Components, Casting Time, etc.
- **Item/Weapon Cards** – ID, Name, Price, Weight, Damage, Attributes, Versatile damage
- **Armor Cards** – ID, Name, Price, Weight, Armor Class and category

Monster cards and enchantments are planned for future releases.

## Contributing

Bug reports and pull requests are welcome on the `main` branch. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for code style and guidelines.

## License

This project is released under the Creative Commons BY-NC-SA 4.0 license. Private use and modifications are allowed; commercial use requires prior permission.

## Acknowledgements & Contact

Thanks to anyone considering contributing data and ideas, your feedback is much appreciated. For questions or feedback open an issue on GitHub.

**Have Fun!** ~yoshi-qq
