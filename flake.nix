{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python310Packages;
      in rec {
        packages = rec {
          default = refactoo;

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
              # python3 -m unittest discover -v -s tests/
              runHook postCheck
            '';

            propagatedBuildInputs = [
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
