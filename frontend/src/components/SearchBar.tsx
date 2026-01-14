"use client";

import { Search, X, ChevronRight } from "lucide-react";

interface SearchBarProps {
    value: string;
    onChange: (value: string) => void;
    onSearch?: () => void;
    placeholder?: string;
    loading?: boolean;
    showButton?: boolean;
    className?: string;
}

export default function SearchBar({
    value,
    onChange,
    onSearch,
    placeholder = "Search by dish name...",
    loading = false,
    showButton = false,
    className = ""
}: SearchBarProps) {
    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && onSearch) {
            onSearch();
        }
    };

    return (
        <div className={`search-bar-modern glass-panel highlight-on-focus ${showButton ? 'with-button' : ''} ${className}`}>
            <Search className="search-icon" size={22} />
            <input
                type="text"
                className="search-input-modern"
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
            />

            {value && (
                <button
                    className="clear-btn"
                    onClick={() => onChange("")}
                    aria-label="Clear search"
                    type="button"
                >
                    <X size={18} />
                </button>
            )}

            {loading && <div className="spinner-small" />}

            {showButton && onSearch && (
                <button
                    onClick={onSearch}
                    className="search-btn"
                    aria-label="Submit search"
                    type="button"
                >
                    <ChevronRight size={24} />
                </button>
            )}
        </div>
    );
}
