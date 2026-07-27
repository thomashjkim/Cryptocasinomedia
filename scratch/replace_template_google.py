file_path = "/Users/thomaskim/Cryptocasinomedia/index/index.html.template"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """if (company.includes("Polymarket") || company.includes("Kalshi") || company.includes("CFTC")) {
                                                  return `${company} represent leading digital prediction platforms and CFTC-regulated event-contract exchanges. These protocols or sportsbooks facilitate peer-to-peer wagering and structured hedging on global events.`;
                                              } else if (company.includes(",") || company.includes("&") || company.includes(" and ")) {
                                                  return `The platforms and operators referenced (${company}) represent leading operators, technology vendors, or compliance services operating within the digital asset and interactive gaming space.`;
                                              } else {
                                                  return `${company} is a leading operator in the digital asset and interactive gaming space, committed to providing secure, transparent, and innovative entertainment experiences globally. For more information, visit the official corporate portal.`;
                                              }"""

replacement = """if (company.includes("Polymarket") || company.includes("Kalshi") || company.includes("CFTC")) {
                                                  return `${company} represent leading digital prediction platforms and CFTC-regulated event-contract exchanges. These protocols or sportsbooks facilitate peer-to-peer wagering and structured hedging on global events.`;
                                              } else if (company.includes("Google") || company.includes("Alphabet")) {
                                                  return `Google (Alphabet Inc.) is a global technology leader, specializing in search engine platforms, digital advertising, and cloud computing infrastructure, defining advertising policy and compliance standards globally.`;
                                              } else if (company.includes(",") || company.includes("&") || company.includes(" and ")) {
                                                  return `The platforms and operators referenced (${company}) represent leading operators, technology vendors, or compliance services operating within the digital asset and interactive gaming space.`;
                                              } else {
                                                  return `${company} is a leading operator in the digital asset and interactive gaming space, committed to providing secure, transparent, and innovative entertainment experiences globally. For more information, visit the official corporate portal.`;
                                              }"""

if target in content:
    content = content.replace(target, replacement)
    print("Replacement successful!")
else:
    target_esc = target.replace("${company}", "\\${company}").replace("(${company})", "(\\${company})")
    replacement_esc = replacement.replace("${company}", "\\${company}").replace("(${company})", "(\\${company})")
    if target_esc in content:
        content = content.replace(target_esc, replacement_esc)
        print("Replacement (escaped) successful!")
    else:
        print("Target block not found in file!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
