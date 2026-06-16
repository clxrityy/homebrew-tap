cask "licensor" do
    version "0.3.1"
    sha256 "d41c9ea7607594fae38f8f879ddb50941218a3e4f586a42d2ad45fa05b41b576"

    url "https://github.com/clxrityy/Licensor/releases/download/v#{version}/Licensor_#{version}_universal.dmg"
    name "Licensor"
    desc "Desktop app for managing document templates with variable substitution, rendering, and export"
    homepage "https://github.com/clxrityy/Licensor"

    depends_on macos: ">= :catalina"

    app "Licensor.app"

    zap trash: [
        "~/Library/Application Support/com.mjanglin.licensor",
        "~/Library/Caches/com.mjanglin.licensor",
    ]
end
