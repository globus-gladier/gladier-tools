# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.3.3](https://github.com/globus-gladier/gladier_tools/compare/v0.3.2...v0.3.3) (2021-11-17)


### Bug Fixes

* Encrypt Tools imports not being top level ([38d1c88](https://github.com/globus-gladier/gladier_tools/commit/38d1c88884a1bb11a28a1409cc18df9c77b4405e))

### [0.3.2](https://github.com/globus-gladier/gladier_tools/compare/v0.3.1...v0.3.2) (2021-11-15)


### Bug Fixes

* Fix publish raising custom exceptions, add unit tests ([#37](https://github.com/globus-gladier/gladier_tools/issues/37)) ([90fc22a](https://github.com/globus-gladier/gladier_tools/commit/90fc22ad66dc72ead1196e910b6bb054227c397f))

### [0.3.1](https://github.com/globus-gladier/gladier_tools/compare/v0.3.0...v0.3.1) (2021-08-05)


### Features

* Add encrypt/decrypt tools [#20](https://github.com/globus-gladier/gladier_tools/issues/20) ([7a62684](https://github.com/globus-gladier/gladier_tools/commit/7a62684519c939faaeafb2f2def76b53ddd5d578))
* Added asymmetrical encrypt/decrypt tools [#32](https://github.com/globus-gladier/gladier_tools/issues/32) ([97f308e](https://github.com/globus-gladier/gladier_tools/commit/97f308e259fe426c30deb76d024761c1e34c0ff6))


### Bug Fixes

* Bug when tar_input on Tar Tool had a trailing slash ([#36](https://github.com/globus-gladier/gladier_tools/issues/36)) ([98ac3f2](https://github.com/globus-gladier/gladier_tools/commit/98ac3f2e3fce9fa48d31beffc6de4da44306f802))
* Fixed tar incorrect file hierarchy ([3b62d86](https://github.com/globus-gladier/gladier_tools/commit/3b62d86b358c438063ced96b92331a437a552b27))

## [0.3.0](https://github.com/globus-gladier/gladier_tools/compare/v0.2.1...v0.3.0) (2021-07-19)


### ⚠ BREAKING CHANGES

* Introduces lots of backward incompaible funcx changes
in FuncX 0.2.3+

### Features

* Update to Gladier v4 ([#18](https://github.com/globus-gladier/gladier_tools/issues/18)) ([b21dd90](https://github.com/globus-gladier/gladier_tools/commit/b21dd905495928f0af22f3380c261e8fcd1da9cd))

### [0.2.1](https://github.com/globus-gladier/gladier_tools/compare/v0.2.0...v0.2.1) (2021-07-13)


### Bug Fixes

* Tar not archiving paths correctly ([d5d9dec](https://github.com/globus-gladier/gladier_tools/commit/d5d9deca74320c6a9f3ddef2dd319c2c88785bcb))

## [0.2.0](https://github.com/globus-gladier/gladier_tools/compare/v0.1.0...v0.2.0) (2021-07-06)


### Features

* Added 'publish' tool for publication using globus-pilot ([#14](https://github.com/globus-gladier/gladier_tools/issues/14)) ([54bf2f6](https://github.com/globus-gladier/gladier_tools/commit/54bf2f647ab4f1cd5dc8275681694f0565d79418))

## 0.0.0

### 0.0.1 - Apr 5, 2021

- Initial Release!
- This allows for very basic reprocessing using Manifests. This is the first live
Reprocessing flow third party users can invoke from petreldata.net.