# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
Unreleased changes will be added to this section first.


## [2.2.2] - 2021-12-15
### Added
- Added a telegram notification when the app has been launched.

[2.2.2]: https://github.com/resolator/rpi-surveillance/compare/v2.2.1...v2.2.2


## [2.2.1] - 2021-12-07
### Added
- Added camera release when closing the application.

[2.2.1]: https://github.com/resolator/rpi-surveillance/compare/v2.2.0...v2.2.1


## [2.2.0] - 2021-07-07
### Added
- Additional argument `--detection-frames` for motion detection.

### Changed
- Motion detection improved for cases with camera noise.

[2.2.0]: https://github.com/resolator/rpi-surveillance/compare/v2.1.0...v2.2.0


## [2.1.0] - 2021-07-07
### Added
- Motion detection argumets.

### Removed
- Unused telegram pooling.

[2.1.0]: https://github.com/resolator/rpi-surveillance/compare/v2.0.1...v2.1.0


## [2.0.1] - 2021-06-29
### Changed
- Temporary directory mount rights.

[2.0.1]: https://github.com/resolator/rpi-surveillance/compare/v2.0.0...v2.0.1


## [2.0.0] - 2021-06-29
### Added
- Temporary directory cleanup when starting the work.

### Changed
- Distribution way (developed debian package).
- Moved tmpfs creation to the installation stage.

[2.0.0]: https://github.com/resolator/rpi-surveillance/compare/v1.0.0...v2.0.0


## [1.0.0] - 2021-06-21
Initial release.

[1.0.0]: https://github.com/resolator/rpi-surveillance/releases/tag/v1.0.0
