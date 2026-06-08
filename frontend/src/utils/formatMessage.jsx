export function formatMessage(text) {
  const lines = text.split("\n").filter(Boolean);

  const result = [];

  lines.forEach((line, i) => {
    const trimmed = line.trim();

    const isBullet =
      trimmed.startsWith("- ") ||
      trimmed.startsWith("* ") ||
      /^\d+\./.test(trimmed);

    if (isBullet) {
      result.push({
        type: "li",
        text: trimmed.replace(/^[-*]\s|^\d+\.\s/, "")
      });
    } else {
      result.push({
        type: "p",
        text: trimmed
      });
    }
  });

  return result;
}