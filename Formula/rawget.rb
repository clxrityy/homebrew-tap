class Rawget < Formula
  include Language::Python::Virtualenv

  desc "Lightweight CLI tool for downloading files from URLs"
  homepage "https://github.com/clxrityy/rawget"
  url "https://files.pythonhosted.org/packages/4c/f9/df56df98fc83fe723d4e9d63c94a065e82127af2522971d60fded704b184/rawget-0.11.2.tar.gz"
  sha256 "70eeb920382726bc8e919b3de94df660f70f9a73b6f75dae0c459f5555db51b3"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"rawget", "--help"
  end
end
