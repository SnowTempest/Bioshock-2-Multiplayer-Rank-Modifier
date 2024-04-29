# Bioshock 2 Multiplayer Rank Modifier

## Description

The Bioshock 2 Multiplayer Rank Modifier is a program designed to allow User's to modify their Rank in Bioshock 2 Multiplayer.

## Features

- **Rank Fix**: Automatically adjusts User's mRankAdamRequirements to reach Rank 50 after completing either 1 Public Match or 1 Private Match.
- **Custom Ranks**: Sets a Custom Rank for the User. Up to Rank 1000. (May Most Likely Be Changed in the Future)
- **Default Rank**: Reverts the mRankAdamRequirements back to their default values. Note: This will reset the User's Rank to 50 if they have over 163000 Adam.

## Disclaimer

- Please note that using Custom Ranks will not provide you with any gameplay advantage. Ranks exceeding 50 are purely cosmetic and do not affect gameplay in any way.
- Other players can see your Custom Rank. If you prefer not to display a Rank higher than 50, utilize the Rank Fix feature to reset your Rank back to 50.
- Custom Ranks do not unlock any additional content beyond what is available through normal gameplay. All unlocks are typically accessible once the player reaches Rank 50.

## Modified Files

- **ShockMPGame.ini**: This file is used to determine the mRankAdamRequirements for Ranks 0 - 40.
- **dlc1unlocks.ini**: This file is used to determine the mRankAdamRequirements for Ranks 41 - 50.
- **dlc2unlocks.ini**: This file is also used to determine the mRankAdamRequirements for Ranks 41 - 50. However, this file is used for setting User's Custom Ranks.

## Usage

1. **Download**: Download the program from the "Releases" section of the GitHub repository.
2. **Run**: Execute the program and follow the on-screen prompts to choose the desired feature.
3. **Launch Game**: Open Bioshock 2 Multiplayer to ensure the game files are located.
4. **Follow Prompts**: Continue following the prompts until the program completes its tasks.
5. **Restart Game**: Restart Bioshock 2 Multiplayer to apply the changes.

## Screenshots

![Custom Rank In-Game](https://github.com/SnowTempest/Bioshock-2-Multiplayer-Rank-Modifier/blob/main/Screenshots/level100.jpg)

## Libraries

### 1. Psutil

- **Documentation**: [Psutil Documentation](https://pypi.org/project/psutil/)
- **Description**: Enables access to process information for enhanced functionality.

## License

This project is licensed under the [Creative Commons Zero v1.0 Universal License](LICENSE).
