{ pkgs, lib, config, inputs, ... }:
let
  pythonPackage = pkgs.python310;
in
{
  dotenv.disableHint = true;

  packages = [
    pkgs.nodejs_18
    pkgs.just
    pkgs.dig
  ];

  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      package = pythonPackage;
      poetry = {
        enable = true;
      };
    };
  };
}