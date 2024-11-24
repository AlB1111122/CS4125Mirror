{
  description = "CS4125: Lab04";

  inputs = {
    utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    utils,
  }:
    utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages."${system}";
        # find these here https://search.nixos.org/packages?channel=unstable&from=0&size=50&sort=relevance&type=packages&query=python312Packages.mkdocs
        packages = [
          pkgs.python3
        ] ++ (with pkgs.python3Packages; [
          numpy
          pandas
          scikit-learn
          stanza
          transformers
          sentencepiece
        ]);
      in {
        devShells.default = pkgs.mkShell {
          name = "CS4125: Project";
          packages = packages;
        };
      }
    );
}
