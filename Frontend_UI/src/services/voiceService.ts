/**
 * Text-to-Speech Voice Service
 * Handles Indian accent voice with 1.5x speed as requested
 */

export interface VoiceSettings {
  rate: number; // 1.5x speed
  pitch: number;
  volume: number;
}

const VOICE_SETTINGS: Record<string, VoiceSettings> = {
  aggressive: {
    rate: 1.5, // Fast, energetic
    pitch: 1.1,
    volume: 1.0,
  },
  balanced: {
    rate: 1.5, // Standard fast speed
    pitch: 1.0,
    volume: 1.0,
  },
  safe: {
    rate: 1.5, // Still fast, but cautious
    pitch: 0.95,
    volume: 0.9,
  },
};

/**
 * Speak text with Indian English voice at 1.5x speed
 * Automatically plays when message appears
 */
export function speakWithIndianAccent(
  text: string,
  agentType: "aggressive" | "balanced" | "safe" = "balanced"
): Promise<void> {
  return new Promise((resolve, reject) => {
    if (!("speechSynthesis" in window)) {
      reject(new Error("Speech Synthesis not supported"));
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const settings = VOICE_SETTINGS[agentType];

    // Find Indian English voice
    const voices = speechSynthesis.getVoices();
    let selectedVoice = voices.find(
      (v) => v.lang === "en-IN" || v.lang.startsWith("hi")
    );

    // Fallback to any English voice if Indian not found
    if (!selectedVoice) {
      selectedVoice = voices.find((v) => v.lang.startsWith("en"));
    }

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.lang = "en-IN";
    utterance.rate = settings.rate; // 1.5x speed
    utterance.pitch = settings.pitch;
    utterance.volume = settings.volume;

    utterance.onend = () => resolve();
    utterance.onerror = (error) => reject(error);

    speechSynthesis.speak(utterance);
  });
}

/**
 * Cancel all ongoing speech
 */
export function cancelSpeech(): void {
  if ("speechSynthesis" in window) {
    speechSynthesis.cancel();
  }
}

/**
 * Check if speech synthesis is available
 */
export function isSpeechSynthesisAvailable(): boolean {
  return "speechSynthesis" in window;
}

/**
 * Pre-load voices (needed for some browsers)
 */
export function preloadVoices(): void {
  if ("speechSynthesis" in window) {
    speechSynthesis.getVoices();
  }
}
