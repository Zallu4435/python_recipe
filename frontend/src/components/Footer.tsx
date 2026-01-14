import Link from 'next/link';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="container footer-content">
                <div className="footer-brand">
                    <span className="logo-text">Become-A-Cook</span>
                    <p>Elevate your culinary instincts with AI-powered puzzles.</p>
                </div>
                <div className="footer-links">
                    <Link href="/">Home</Link>
                    <Link href="/search">Challenges</Link>
                    <Link href="#">About</Link>
                </div>
                <div className="footer-bottom">
                    <p>&copy; {new Date().getFullYear()} Become-A-Cook AI. Built with passion for food.</p>
                </div>
            </div>
        </footer>
    );
}
