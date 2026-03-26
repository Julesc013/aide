# Current Xcode Notes

Primary sources: [Xcode overview](https://developer.apple.com/xcode), [Xcode support matrix](https://developer.apple.com/support/xcode), [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/).

## Facts as of 2026-03-27

- Apple's current Xcode page says Xcode includes predictive code completion, "generative intelligence powered by the best coding models and agents," and Coding Tools in the source editor.
- Apple's support matrix lists Xcode 26 as the latest family and still lists Xcode 16 as a current older family.
- Apple's Upcoming Requirements page says App Store Connect submissions must use Xcode 26 or later beginning on April 28, 2026. Until that date, the earlier Xcode 16 floor from April 24, 2025 remains the active published requirement.

## Architectural effect on AIDE

- Current Xcode already includes first-party coding assistance. Any future AIDE Xcode work should assume coexistence with Apple's built-in assistance rather than an empty editor-assistance space.
- Current Apple distribution policy makes current-family relevance matter. AIDE should not assume that very old Xcode families remain useful for shipping workflows even if they still matter for archival research.

## Inference

- The combination of a narrow public XcodeKit surface and increasingly capable first-party Xcode assistance makes it reasonable for AIDE to keep Apple-native ambitions conservative and companion-oriented where broader workflows are needed.
