class GitAutoDescribe < Formula
  include Language::Python::Virtualenv

  desc "Generate commit messages using ML"
  homepage "https://github.com/Zithrill/ZScribe"
  url "https://github.com/Zithrill/ZScribe/archive/v0.1.0.tar.gz"
  sha256 "INSERT_SHA256_HERE"  # You'll need to calculate this when you have a release

  depends_on "python@3.9"

  resource "anthropic" do
    url "https://files.pythonhosted.org/packages/SOURCE_URL_FOR_ANTHROPIC_PACKAGE"
    sha256 "INSERT_SHA256_HERE"  # You'll need to get this from the actual package
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage: git-commit-message-generator", shell_output("#{bin}/git-commit-message-generator --help")
  end
end