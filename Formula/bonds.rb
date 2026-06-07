class Bonds < Formula
  desc "CLI for creating and managing symlink-based bonds"
  homepage "https://bonds.fyi"
  url "https://static.crates.io/crates/bonds-cli/bonds-cli-0.1.7.crate"
  sha256 "cacfb5255eb1e7c78a115e7d0fb83e995853eb52b23e87a63e6427bac85e8d3c"
  license "GPL-3.0-only"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args
  end

  test do
    (testpath/"source").mkpath

    system bin/"bond", "add", testpath/"source", testpath/"target", "--name", "homebrew-test"

    assert_predicate testpath/"target", :symlink?

    output = shell_output("#{bin}/bond list")
    assert_match "All Bonds:", output
    assert_match "homebrew-test", output
    assert_match "1 bond(s) total.", output
  end
end
