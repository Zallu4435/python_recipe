"use client";

import { useEffect, useState, Suspense, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useDebounce } from "use-debounce";
import { Search, SlidersHorizontal, LayoutGrid, List, Sparkles, X, ChevronDown, Check, Filter } from "lucide-react";
import Loading from "@/components/Loading";
import RecipeCard from "@/components/RecipeCard";
import Pagination from "@/components/Pagination";
import SearchBar from "@/components/SearchBar";

import { API_BASE_URL } from "@/lib/config";

interface Recipe {
    id: number;
    name: string;
    image: string;
}

const CATEGORIES = [
    "All", "Beef", "Chicken", "Dessert", "Lamb", "Miscellaneous", "Pasta",
    "Pork", "Seafood", "Side", "Starter", "Vegan", "Vegetarian", "Goat"
];

function SearchContent() {
    const searchParams = useSearchParams();
    const router = useRouter();

    const queryParam = searchParams.get("q") ?? "";
    const categoryParam = searchParams.get("category") ?? "All";

    const [inputValue, setInputValue] = useState(queryParam);
    const [debouncedQuery] = useDebounce(inputValue, 500);

    const [selectedCategory, setSelectedCategory] = useState(categoryParam);
    const [isFilterOpen, setIsFilterOpen] = useState(false);
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
    const filterRef = useRef<HTMLDivElement>(null);

    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [status, setStatus] = useState<'loading' | 'idle' | 'error'>('loading');
    const [page, setPage] = useState(parseInt(searchParams.get("page") ?? "1"));
    const [totalPages, setTotalPages] = useState(1);

    // Sync input with URL param (e.g. when clicking a suggestion or using back btn)
    useEffect(() => {
        if (queryParam !== inputValue) {
            setInputValue(queryParam);
        }
    }, [queryParam]);

    // Close filter when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (filterRef.current && !filterRef.current.contains(event.target as Node)) {
                setIsFilterOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    // Lock body scroll on mobile when filter is open
    useEffect(() => {
        const checkScrollLock = () => {
            if (isFilterOpen && window.innerWidth <= 640) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        };

        checkScrollLock();
        window.addEventListener('resize', checkScrollLock);
        return () => {
            window.removeEventListener('resize', checkScrollLock);
            document.body.style.overflow = '';
        };
    }, [isFilterOpen]);

    // Update URL when filters change
    useEffect(() => {
        const params = new URLSearchParams(searchParams);
        if (debouncedQuery) params.set("q", debouncedQuery); else params.delete("q");
        if (selectedCategory && selectedCategory !== "All") params.set("category", selectedCategory); else params.delete("category");
        if (page > 1) params.set("page", page.toString()); else params.delete("page");

        router.replace(`/search?${params.toString()}`, { scroll: false });
    }, [debouncedQuery, selectedCategory, page]);

    // Reset page when search criteria change
    useEffect(() => {
        if (page !== 1) setPage(1);
    }, [debouncedQuery, selectedCategory]);

    useEffect(() => {
        const fetchRecipes = async () => {
            setStatus('loading');
            try {
                let url = `${API_BASE_URL}/recipes/search?q=${encodeURIComponent(debouncedQuery)}&page=${page}&limit=12`;
                if (selectedCategory && selectedCategory !== "All") {
                    url += `&category=${encodeURIComponent(selectedCategory)}`;
                }

                const res = await fetch(url);
                if (!res.ok) throw new Error("Failed to fetch");
                const data = await res.json();

                if (data.items) {
                    setRecipes(data.items);
                    setTotalPages(data.totalPages);
                } else {
                    setRecipes(data || []);
                    setTotalPages(1);
                }
                setStatus('idle');
            } catch (err) {
                console.error(err);
                setRecipes([]);
                setStatus('error');
            }
        };

        fetchRecipes();
    }, [debouncedQuery, selectedCategory, page]);

    const clearFilters = () => {
        setInputValue("");
        setSelectedCategory("All");
        setPage(1);
    };

    return (
        <div className="search-page-container">
            {/* Search Hero Header */}
            <header className="search-header">
                <div className="container">
                    <div className="search-header-content animate-fade-in">
                        <div className="badge animate-float">
                            <Sparkles size={14} />
                            <span>Challenge Library</span>
                        </div>
                        <h1 className="search-title mt-2">Find Your Next <span className="text-primary-gradient">Culinary Puzzle</span></h1>
                        <p className="search-description">Choose a dish and test your cooking instincts. Over {recipes.length > 0 ? '1,000+' : 'hundreds of'} AI-curated recipes await.</p>
                    </div>

                    <div className="search-controls-wrapper animate-fade-in" style={{ animationDelay: '0.1s' }}>
                        <SearchBar
                            value={inputValue}
                            onChange={setInputValue}
                            loading={status === 'loading'}
                            placeholder="Search by name (e.g. Pasta, Burger)..."
                        />
                    </div>
                </div>
                <div className="cta-decoration animate-float-slow" style={{ top: '20%', right: '5%' }}>
                    <Search size={160} />
                </div>
            </header>

            {/* Results Section */}
            <main className="search-results-main container">
                <div
                    className="results-meta animate-fade-in-opacity"
                    style={{
                        animationDelay: '0.2s',
                        zIndex: isFilterOpen ? 2000 : 100
                    }}
                >
                    <div className="results-count">
                        {status === 'loading' && recipes.length === 0 ? (
                            'Scanning library...'
                        ) : (
                            <>
                                Found <strong>{recipes.length}</strong> results
                                {debouncedQuery && <> for "<strong>{debouncedQuery}</strong>"</>}
                                {selectedCategory !== "All" && <> in <strong>{selectedCategory}</strong></>}
                            </>
                        )}
                    </div>

                    <div className="results-actions">
                        {/* Pagination at the top */}
                        {status !== 'loading' && totalPages > 1 && (
                            <div className="compact-pagination-wrapper">
                                <Pagination
                                    page={page}
                                    totalPages={totalPages}
                                    setPage={setPage}
                                />
                            </div>
                        )}

                        {/* ABSOLUTE POSITIONED FILTER */}
                        <div className="filter-dropdown-container" ref={filterRef}>
                            <button
                                className={`icon-btn ${selectedCategory !== "All" ? 'active' : ''}`}
                                onClick={() => setIsFilterOpen(!isFilterOpen)}
                                aria-expanded={isFilterOpen}
                            >
                                <Filter size={18} />
                                <span>{selectedCategory === "All" ? "Filter" : selectedCategory}</span>
                                <ChevronDown size={14} className={`dropdown-arrow ${isFilterOpen ? 'open' : ''}`} />
                            </button>

                            {isFilterOpen && (
                                <>
                                    <div className="absolute-filter-panel glass-panel animate-scale-in">
                                        <div className="filter-header">
                                            <span>Categories</span>
                                            <button onClick={() => setIsFilterOpen(false)} aria-label="Close filters">
                                                <X size={14} />
                                            </button>
                                        </div>
                                        <div className="filter-options-grid">
                                            {CATEGORIES.map(cat => (
                                                <button
                                                    key={cat}
                                                    className={`filter-option ${selectedCategory === cat ? 'selected' : ''}`}
                                                    onClick={() => {
                                                        setSelectedCategory(cat);
                                                        setIsFilterOpen(false);
                                                    }}
                                                >
                                                    <span>{cat}</span>
                                                    {selectedCategory === cat && <Check size={14} />}
                                                </button>
                                            ))}
                                        </div>
                                        {selectedCategory !== "All" && (
                                            <button className="reset-filter-btn" onClick={() => {
                                                setSelectedCategory("All");
                                                setIsFilterOpen(false);
                                            }}>
                                                Reset to All
                                            </button>
                                        )}
                                    </div>
                                    {/* Subtle overlay to help focus on filter */}
                                    <div className="filter-backdrop" onClick={() => setIsFilterOpen(false)} />
                                </>
                            )}
                        </div>

                        <div className="view-toggle">
                            <button
                                className={`icon-btn ${viewMode === 'grid' ? 'active' : ''}`}
                                onClick={() => setViewMode('grid')}
                                aria-label="Grid View"
                            >
                                <LayoutGrid size={18} />
                            </button>
                            <button
                                className={`icon-btn ${viewMode === 'list' ? 'active' : ''}`}
                                onClick={() => setViewMode('list')}
                                aria-label="List View"
                            >
                                <List size={18} />
                            </button>
                        </div>
                    </div>
                </div>

                <div className="search-grid-wrapper">
                    {status === 'loading' && recipes.length === 0 ? (
                        <div className="grid-layout">
                            {Array(8).fill(0).map((_, i) => (
                                <div key={i} className="recipe-card-skeleton glass-panel" style={{ height: '320px' }} />
                            ))}
                        </div>
                    ) : recipes.length > 0 ? (
                        <div className={`${viewMode === 'grid' ? 'grid-layout' : 'list-layout'} animate-fade-in`} style={{ animationDelay: '0.3s' }}>
                            {recipes.map((recipe, index) => (
                                <RecipeCard
                                    key={`${recipe.id}-${selectedCategory}-${viewMode}`}
                                    id={recipe.id}
                                    name={recipe.name}
                                    image={recipe.image}
                                    className={viewMode === 'list' ? 'list-item-card' : ''}
                                    style={{ animationDelay: `${0.03 * (index % 12)}s` }}
                                />
                            ))}
                        </div>
                    ) : status === 'idle' ? (
                        <div className="no-results animate-fade-in">
                            <div className="no-results-icon">🤷‍♂️</div>
                            <h3>No matches found</h3>
                            <p>We couldn't find any challenges for your current filters. Try broader terms or reset everything.</p>
                            <button className="btn-secondary mt-4" onClick={clearFilters}>
                                Reset Search & Filters
                            </button>
                        </div>
                    ) : (
                        <div className="error-state animate-fade-in">
                            <h3>Something went wrong</h3>
                            <p>We're having trouble reaching the Chef. Please try again later.</p>
                            <button className="btn-primary mt-4" onClick={() => window.location.reload()}>
                                Reload Page
                            </button>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default function SearchPage() {
    return (
        <Suspense fallback={<Loading />}>
            <SearchContent />
        </Suspense>
    );
}
