'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X, ChefHat, Sparkles, Home, UtensilsCrossed } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Navbar() {
    const pathname = usePathname();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const toggleMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

    const isActive = (path: string) => pathname === path;

    const navLinks = [
        { name: 'Home', href: '/', icon: <Home size={24} /> },
        { name: 'Challenges', href: '/search', icon: <UtensilsCrossed size={24} /> },
    ];

    return (
        <nav className={`navbar-modern ${scrolled ? 'is-scrolled' : ''}`}>
            <div className="navbar-container">
                <Link href="/" className="navbar-brand">
                    <div className="brand-icon-wrapper">
                        <ChefHat size={22} className="brand-icon" />
                    </div>
                    <span className="brand-name">
                        Become<span className="text-primary-gradient">A</span>Cook
                    </span>
                </Link>

                <div className="nav-navigation">
                    <div className="nav-items-wrapper">
                        {navLinks.map((link) => (
                            <Link
                                key={link.name}
                                href={link.href}
                                className={`nav-item ${isActive(link.href) ? 'is-active' : ''}`}
                            >
                                {link.name}
                                {isActive(link.href) && <div className="active-indicator" />}
                            </Link>
                        ))}
                    </div>
                </div>

                <div className="nav-extra">
                    <Link href="/search" className="navbar-cta">
                        <Sparkles size={16} />
                        <span>Start Cooking</span>
                    </Link>

                    <button className="navbar-mobile-toggle" onClick={toggleMenu} aria-label="Toggle Menu">
                        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>

                {/* Mobile Menu */}
                <div className={`navbar-mobile-menu ${isMobileMenuOpen ? 'is-open' : ''}`}>
                    <div className="mobile-menu-content">
                        {navLinks.map((link, index) => (
                            <div key={link.name} className="flex-center flex-column" style={{ width: '100%' }}>
                                <Link
                                    href={link.href}
                                    className={`mobile-nav-item ${isActive(link.href) ? 'is-active' : ''}`}
                                    onClick={() => setIsMobileMenuOpen(false)}
                                >
                                    <div className="mobile-nav-icon">{link.icon}</div>
                                    <span className="mobile-nav-text">{link.name}</span>
                                </Link>
                                {index < navLinks.length - 1 && <div className="mobile-menu-divider" />}
                            </div>
                        ))}
                        <div className="mobile-menu-footer">
                            <Link
                                href="/search"
                                className="navbar-cta full-width"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                <Sparkles size={18} />
                                <span>Get Started</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}
