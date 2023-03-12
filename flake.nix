{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";

    comby_src.url = "github:ChrisTimperley/comby-python?ref=v0.3.0";
    comby_src.flake = false;
  };

  outputs = { self, nixpkgs, flake-utils, comby_src }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python310Packages;
      in rec {
        packages = rec {
          default = refactoo;

          comby = pythonPackages.buildPythonPackage {
            name = "comby";
            version = "0.3.0";
            src = comby_src;

            doCheck = false;

            patchPhase = ''
              sed -i '/typing >= 0.4/d' setup.cfg
            '';

            propagatedBuildInputs = [
              pythonPackages.typing
              pythonPackages.requests
              pythonPackages.loguru
              pythonPackages.attrs
            ];
          };

          refactoo = pythonPackages.buildPythonPackage rec {
            pname = "refactoo";
            version = "0.0.0";

            src = ./.;

            doCheck = true;

            checkPhase = ''
              runHook preCheck
              flake8 --max-line-length=120
              mypy -p refactoo  # -p tests
              pylint refactoo  # tests
              python3 -m unittest discover -v -s tests/
              runHook postCheck
            '';

            propagatedBuildInputs = [
              comby
              pkgs.comby
            ];

            checkInputs = [
              pythonPackages.flake8
              pythonPackages.mypy
              pythonPackages.pylint
              pythonPackages.types-setuptools
              pythonPackages.pip
            ];
          };
        };
      }
    );
}
