class Gatenet < Formula
  include Language::Python::Virtualenv

  desc "Python library for gateways, networks, and devices"
  homepage "https://github.com/clxrityy/gatenet"
  url "https://pypi.org/packages/source/g/gatenet/gatenet-0.12.5.tar.gz"
  sha256 "c025a80e75a595f7a3679ef1b0cd5b3f0294b176680f3763284a96c3cfc8708e"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    # Test that the module can be imported using the virtual environment Python
    system libexec/"bin/python", "-c", "import gatenet; print('gatenet imported successfully')"
  end
end
