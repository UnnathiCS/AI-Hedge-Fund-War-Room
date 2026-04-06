export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-12 py-6 px-4 border-t border-secondary/30 bg-background/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col items-center justify-center gap-2">
          <p className="text-sm text-muted-foreground">
            Built with <span className="text-red-500">❤️</span> by{" "}
            <a
              href="https://github.com/UnnathiCS"
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-foreground hover:text-primary transition-colors"
            >
              UnnathiCS
            </a>
          </p>
          <p className="text-xs text-muted-foreground/70">
            AI Hedge Fund War Room • © {currentYear} All rights reserved
          </p>
        </div>
      </div>
    </footer>
  );
}
