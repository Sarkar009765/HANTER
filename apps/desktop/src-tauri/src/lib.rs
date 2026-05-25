pub fn get_system_info() -> String {
    let info = serde_json::json!({
        "platform": std::env::consts::OS,
        "arch": std::env::consts::ARCH,
    });
    info.to_string()
}
