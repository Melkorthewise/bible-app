{
  description = "Python dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShells = {
      x86_64-linux = let
        pkgs = import nixpkgs { system = "x86_64-linux"; };
      in {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python3
            python3Packages.numpy
            python3Packages.django
            python3Packages.sentence-transformers
            python3Packages.pip
            python3Packages.setuptools
            python3Packages.wheel
          ];

          shellHook = ''
            echo "🔧 Python dev environment activated!"
          '';
        };
      };
    };
  };
}

