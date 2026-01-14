import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

interface PaginationProps {
    page: number;
    totalPages: number;
    setPage: (page: number | ((p: number) => number)) => void;
}

export default function Pagination({ page, totalPages, setPage }: PaginationProps) {
    if (totalPages <= 1) return null;

    return (
        <div className="pagination-wrapper-v2">
            <button
                onClick={() => setPage(1)}
                disabled={page === 1}
                className="pagination-arrow-btn"
                title="First Page"
            >
                <ChevronsLeft size={18} />
            </button>
            <button
                onClick={() => setPage((p: number) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="pagination-arrow-btn"
                title="Previous Page"
            >
                <ChevronLeft size={18} />
            </button>

            <div className="pagination-number-info">
                <span className="current-page">{page}</span>
                <span className="total-pages-sep desktop-sep">of</span>
                <span className="total-pages-sep mobile-sep">/</span>
                <span className="total-pages">{totalPages}</span>
            </div>

            <button
                onClick={() => setPage((p: number) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="pagination-arrow-btn"
                title="Next Page"
            >
                <ChevronRight size={18} />
            </button>
            <button
                onClick={() => setPage(totalPages)}
                disabled={page === totalPages}
                className="pagination-arrow-btn"
                title="Last Page"
            >
                <ChevronsRight size={18} />
            </button>
        </div>
    );
}
