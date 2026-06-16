class Rawget < Formula
  include Language::Python::Virtualenv

  desc "Lightweight CLI tool for downloading files from URLs"
  homepage "https://github.com/clxrityy/rawget"
  url "https://files.pythonhosted.org/packages/c3/21/4cb02c630d815b5866b35f3d26dc88de211fd2bab85195e8fd405c56eae7/rawget-0.11.1-py3-none-any.whl"
  sha256 "09edf626bcf57cc4705d992d9c626f822f2e07535e76b6174f675b7aa5a2be14"
  license "MIT"

  depends_on "python@3.10"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"rawget", "--help"
  end
end
