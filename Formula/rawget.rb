class Rawget < Formula
  include Language::Python::Virtualenv

  desc "Lightweight CLI tool for downloading files from URLs"
  homepage "https://github.com/clxrityy/rawget"
  url "https://files.pythonhosted.org/packages/95/3a/4b9f3b6f65728b9bbb95d452d7e523f85262df2578c950ec4097784e05f5/rawget-0.11.1.tar.gz"
  sha256 "09edf626bcf57cc4705d992d9c626f822f2e07535e76b6174f675b7aa5a2be14"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"rawget", "--help"
  end
end
