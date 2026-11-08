import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  themeColor: "#030305",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export const metadata: Metadata = {
  metadataBase: new URL("https://aegisbrain.dev"),
  title: {
    default:
      "AegisBrain - Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory",
    template: "%s | AegisBrain",
  },
  description:
    "Sub-second FTS5 neural recall, deterministic 3-tier local token arbitrage, 24/7 Windows daemon, and remote Telegram CLI operations for AI coding assistants.",
  applicationName: "AegisBrain",
  authors: [{ name: "Priyanshu", url: "https://github.com/PG300604" }],
  generator: "Next.js",
  keywords: [
    "AegisBrain",
    "AI coding agent",
    "autonomous daemon",
    "token arbitrage",
    "FTS5 neural memory",
    "3-tier multi-agent",
    "local model offload",
    "Hermes CLI",
    "Telegram CLI remote",
    "sub-second recall",
    "Antigravity",
    "Claude Code",
    "OpenCode",
    "developer tools",
    "generative engine optimization",
  ],
  referrer: "origin-when-cross-origin",
  creator: "Priyanshu",
  publisher: "AegisBrain",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://aegisbrain.dev",
    title:
      "AegisBrain - Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory",
    description:
      "Sub-second FTS5 neural recall, deterministic 3-tier local token arbitrage, 24/7 Windows daemon, and remote Telegram CLI operations for AI coding assistants.",
    siteName: "AegisBrain",
    images: [
      {
        url: "/assets/architecture-unified.svg",
        width: 1200,
        height: 630,
        alt: "AegisBrain Unified Architecture & 3-Tier Multi-Agent Hierarchy",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title:
      "AegisBrain - Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory",
    description:
      "Sub-second FTS5 neural recall, deterministic 3-tier local token arbitrage, 24/7 Windows daemon, and remote Telegram CLI operations for AI coding assistants.",
    images: ["/assets/architecture-unified.svg"],
    creator: "@PG300604",
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: "https://aegisbrain.dev",
  },
};

const jsonLdGraph = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "@id": "https://aegisbrain.dev/#software",
      name: "AegisBrain",
      operatingSystem: "Windows 10/11, Linux, macOS",
      applicationCategory: "DeveloperApplication",
      description:
        "Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory for AI coding assistants.",
      softwareVersion: "0.4.0",
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "USD",
      },
      license: "https://opensource.org/licenses/MIT",
      downloadUrl: "https://github.com/PG300604/aegis-brain/releases",
      author: {
        "@type": "Person",
        name: "Priyanshu",
        url: "https://github.com/PG300604",
      },
      featureList: [
        "Sub-second FTS5 neural memory recall (<24ms)",
        "Hierarchical 3-tier multi-agent token arbitrage (95%+ cost reduction)",
        "24/7 background daemon with Windows Scheduled Task keepalive",
        "Remote Telegram CLI operations with /type keystroke injection",
        "Whisper 25-second audio chunking shield for long voice instructions",
        "4-decision quality architecture gate with automated coaching loop",
      ],
    },
    {
      "@type": "TechArticle",
      "@id": "https://aegisbrain.dev/#article",
      headline:
        "Deterministic LLM Token Arbitrage & Sub-Second Neural Memory Architecture",
      description:
        "How AegisBrain achieves 24ms neural context recall using SQLite FTS5 and saves 95%+ of frontier model tokens via hierarchical 3-tier multi-agent distillation.",
      datePublished: "2026-11-08T00:00:00Z",
      dateModified: "2026-11-08T18:00:00Z",
      author: {
        "@type": "Person",
        name: "Priyanshu",
        url: "https://github.com/PG300604",
      },
      publisher: {
        "@type": "Organization",
        name: "AegisBrain Open Source",
        logo: {
          "@type": "ImageObject",
          url: "https://aegisbrain.dev/assets/aegis-banner.svg",
        },
      },
      mainEntityOfPage: "https://aegisbrain.dev",
      image: "https://aegisbrain.dev/assets/architecture-unified.svg",
    },
    {
      "@type": "FAQPage",
      "@id": "https://aegisbrain.dev/#faq",
      mainEntity: [
        {
          "@type": "Question",
          name: "How does AegisBrain ensure 24/7 daemon keepalive without reboots or account disruption?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "AegisBrain runs a dedicated background daemon backed by Windows Scheduled Tasks (AegisBrainDaemonKeepAlive) repeating every 5 minutes and upon system startup. It keeps the HTTP :8765 memory endpoints and Telegram bot listener active even if terminal windows are closed, user accounts switch, or the machine reboots.",
          },
        },
        {
          "@type": "Question",
          name: "How does 3-Tier Multi-Agent Token Arbitrage work?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Tier 1 Senior Boss (Gemini 4, Claude Opus, Fable) acts as the high-cognition strategic brain and never writes raw code directly. Tier 2 Junior Boss dispatches heavy implementation tasks to Tier 3 local execution workers (Hermes CLI, Qwen2.5-Coder, Ollama) generating candidate code using free local tokens. Tier 2 and Tier 1 audit candidate code through 4 automated quality gates in an error-reduction coaching loop.",
          },
        },
        {
          "@type": "Question",
          name: "What is the Whisper Chunking Shield in Telegram operations?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Voice messages sent to the Aegis Telegram bot longer than 25 seconds are automatically sliced into 25-second overlapping audio segments via FFmpeg before local Whisper model processing, preventing GPU OOM errors and ensuring zero dropped voice instructions.",
          },
        },
        {
          "@type": "Question",
          name: "How does FTS5 Neural Memory achieve sub-second recall?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Instead of crawling multi-megabyte raw JSONL session logs on every prompt (taking 12,400ms+), AegisBrain maintains an indexed SQLite FTS5 neural memory database (brain.db) achieving sub-second BM25 semantic searches in under 24ms.",
          },
        },
      ],
    },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdGraph) }}
        />
      </head>
      <body className="min-h-full flex flex-col bg-[#030305] text-[#E2E8F0] selection:bg-cyan-500/30 selection:text-cyan-200 antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
