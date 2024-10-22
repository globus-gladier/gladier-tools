# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.5.4](https://github.com/globus-gladier/gladier_tools/compare/v0.5.3...v0.5.4) (2024-10-22)


### Bug Fixes

* Update old transfer AP ([c5721e6](https://github.com/globus-gladier/gladier_tools/commit/c5721e62e4ce732efc498b323083580060e50194))

**NOTE** This update contains a fix for upgrading to the newer Transfer Action Provider. The old Transfer Action Provider will be removed Nov 13th, 2024. All users must upgrade.

https://docs.globus.org/api/transfer/action-providers/migration/

### [0.5.3](https://github.com/globus-gladier/gladier_tools/compare/v0.5.2...v0.5.3) (2024-04-15)


### Bug Fixes

* enable_transfer, enabled_publish not working properly ([abd9a72](https://github.com/globus-gladier/gladier_tools/commit/abd9a72cad0e4881d6ff492ddcc0d63ca19ea99d))
* PubishV2 exception with computing checksums if dataset contained nested directories ([f16137f](https://github.com/globus-gladier/gladier_tools/commit/f16137fbab56ff60a0f16226f8436a5f76b8e329))
* Publish v2 not properly picking up subdirectory files ([63d7661](https://github.com/globus-gladier/gladier_tools/commit/63d76617e9f9fbacc5d87bef574cc6d5759cd461))


### [0.5.2](https://github.com/globus-gladier/gladier_tools/compare/v0.5.1...v0.5.2) (2023-09-23)


### Bug Fixes

* Add recursive option to publish v2 ([7f40f4e](https://github.com/globus-gladier/gladier_tools/commit/7f40f4e0d9d8e6b815a7482b80d9ce64ec4e3ba2))

### [0.5.1](https://github.com/globus-gladier/gladier_tools/compare/v0.5.0...v0.5.1) (2023-09-11)


### Features

* Add 'metadata_file' option to publishv2 ([#84](https://github.com/globus-gladier/gladier_tools/issues/84)) ([09fea35](https://github.com/globus-gladier/gladier_tools/commit/09fea35250bbdbc1631517c656fc0588f29fea61))

## [0.5.0](https://github.com/globus-gladier/gladier_tools/compare/v0.4.4...v0.5.0) (2023-08-22)


### ⚠ BREAKING CHANGES

* Update Gladier Tools to require Gladier v0.9.0+
* Upgrade tooling for Gladier v0.9.0

* Update Gladier Tools to require Gladier v0.9.0+ ([e171da3](https://github.com/globus-gladier/gladier_tools/commit/e171da3a36d72c544f33586d9f8ea21eb1a6822d))
* Upgrade tooling for Gladier v0.9.0 ([c359177](https://github.com/globus-gladier/gladier_tools/commit/c35917775816febc93a37a5a99a6d74c7f6d820b))

## [0.5.0b1](https://github.com/globus-gladier/gladier_tools/compare/v0.4.4...v0.5.0b1) (2023-07-11)


### ⚠ BREAKING CHANGES

* RequireGladier v0.9.0+ ([e171da3](https://github.com/globus-gladier/gladier_tools/commit/e171da3a36d72c544f33586d9f8ea21eb1a6822d))


### Features

* Upgrade tooling for Gladier v0.9.0 ([c359177](https://github.com/globus-gladier/gladier_tools/commit/c35917775816febc93a37a5a99a6d74c7f6d820b))

This change upgrades the tools to replace FuncX with Globus Compute as part of Gladier v0.9.0. This also
changes the naming convention of using "funcx_endpoint_compute" and "funcx_endpoint_non_compute". Both have
been changed to "compute_endpoint", and will be used on all future tools.


### [0.4.4](https://github.com/globus-gladier/gladier_tools/compare/v0.4.3...v0.4.4) (2023-04-19)


### Features

* Upgrade to the new Globus Compute action provider ([bf3b2db](https://github.com/globus-gladier/gladier_tools/commit/bf3b2db1f54742dcb9ee8978aa5717629fce99e1))


### [0.4.3](https://github.com/globus-gladier/gladier_tools/compare/v0.4.2...v0.4.3) (2023-04-06)

### Features

* Added new Publishv2 Gladier Tool to replace the old globus-pilot based tool


### [0.4.2](https://github.com/globus-gladier/gladier_tools/compare/v0.4.1...v0.4.2) (2023-03-06)


### Bug Fixes

* Publish bug when a pilot index is set to public ([#67](https://github.com/globus-gladier/gladier_tools/issues/67)) ([8469efe](https://github.com/globus-gladier/gladier_tools/commit/8469efef5f915608040d52fe4a3468a0b1f4c41b))

### [0.4.1](https://github.com/globus-gladier/gladier_tools/compare/v0.4.0...v0.4.1) (2023-01-10)


### Features

* Add guest collection support for publish tool ([#61](https://github.com/globus-gladier/gladier_tools/issues/61)) ([f3a8060](https://github.com/globus-gladier/gladier_tools/commit/f3a8060d05eac661db0de61187a3e1b692f853a3))


### Bug Fixes

* Add shell description to the tool not the function ([#60](https://github.com/globus-gladier/gladier_tools/issues/60)) ([aa980d8](https://github.com/globus-gladier/gladier_tools/commit/aa980d8c44e32a9dc96ab553ed56152701f2f962))
* Ensure untar cannot unpack files outside of specified locations (CVE-2007-4559) ([#57](https://github.com/globus-gladier/gladier-tools/pull/57)) ([f5d11f406](https://github.com/globus-gladier/gladier-tools/pull/57/commits/f5d11f4060f995c745d7628e92b5f67ca6f68ead))  ([#62](https://github.com/globus-gladier/gladier-tools/pull/62))
---


## [0.4.0](https://github.com/globus-gladier/gladier_tools/compare/v0.3.6...v0.4.0) (2022-07-21)


### ⚠ BREAKING CHANGES

* Update Requirements to use Gladier v0.6.3 or higher
    * Older versions of Gladier will no longer be supported

### Features

* Add new POSIX Shell CMD Gladier Tool ([58d49b953](https://github.com/globus-gladier/gladier_tools/commit/58d49b9539d09c24ddf1e2ae1078e91d0b924a6f))

### Other Changes

* Update Requirements to use Gladier v0.6.3 or higher ([4d1c174](https://github.com/globus-gladier/gladier_tools/commit/4d1c17416e6dc5b637f46034f72722ab6f126a2b))

### [0.3.6](https://github.com/globus-gladier/gladier_tools/compare/v0.3.5...v0.3.6) (2021-11-18)

### Bug Fixes

* fix: Decrypt would not expand ~ for custom output files
* fix: encrypt/decrypt tools not raising exceptions on failure

### [0.3.5](https://github.com/globus-gladier/gladier_tools/compare/v0.3.4...v0.3.5) (2021-11-18)

### Bug Fixes

* fix: tar not expanding ~ for output dirs
* fix: untar output dir being incorrectly chosen if not specified

### [0.3.4](https://github.com/globus-gladier/gladier_tools/compare/v0.3.3...v0.3.4) (2021-11-18)


### Bug Fixes

* decrypt raises ValueError on bad key ([#44](https://github.com/globus-gladier/gladier_tools/issues/44)) ([11b52a8](https://github.com/globus-gladier/gladier_tools/commit/11b52a8fb6a98cafdf14c491284666b7234dd2f3))
* Untar using old version of funcx action provider ([#41](https://github.com/globus-gladier/gladier_tools/issues/41)) ([3d6e177](https://github.com/globus-gladier/gladier_tools/commit/3d6e177c7bef920d52061ffa36970a2cdaf5ab55))

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