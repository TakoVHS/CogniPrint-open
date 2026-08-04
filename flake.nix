{
  description = "CogniPrint reproducible local development and packaging environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python312;
      pythonPackages = pkgs.python312Packages;
      cogniprint = pythonPackages.buildPythonApplication {
        pname = "cogniprint";
        version = "0.1.2";
        pyproject = true;
        src = ./.;
        build-system = [ pythonPackages.setuptools ];
        dependencies = [ pythonPackages.pyyaml ];
        doCheck = false;
        pythonImportsCheck = [ "cogniprint" ];
        meta = {
          description = "Local reproducible text-evidence research workstation";
          license = pkgs.lib.licenses.mit;
          mainProgram = "cogniprint";
          platforms = [ system ];
        };
      };
    in
    {
      packages.${system}.default = cogniprint;
      checks.${system}.default = cogniprint;
      apps.${system}.default = {
        type = "app";
        program = "${cogniprint}/bin/cogniprint";
      };
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          (python.withPackages (ps: with ps; [ pyyaml setuptools ]))
          pkgs.git
          pkgs.ruff
        ];
        shellHook = ''
          export PYTHONPATH="$PWD/src''${PYTHONPATH:+:$PYTHONPATH}"
          echo "CogniPrint development shell: Python $(python --version 2>&1)"
        '';
      };
    };
}
