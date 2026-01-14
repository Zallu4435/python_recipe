import { Loader2 } from "lucide-react";

export default function Loading() {
    return (
        <div className="loading-container">
            <Loader2 className="spinner" size={48} color="var(--primary)" />
            <p style={{ fontSize: '1.2rem', fontWeight: 500 }}>Preparing the kitchen...</p>
        </div>
    );
}
