import { useState, useEffect } from "react";

function Reviews() {
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    const variantNumber = 10;
    const apiUrl = `https://jsonplaceholder.typicode.com/posts/${variantNumber}/comments`;

    useEffect(() => {
        async function fetchComments() {
            try {
                setLoading(true);
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }
                const data = await response.json();
                setComments(data);
                setLoading(false);
            } catch (err) {
                console.error("Error comments get:", err);
                setError(true);
                setLoading(false);
            }
        }

        fetchComments();
    }, [apiUrl]);

    return (
        <section className="mt-[40px]">
            <h1 className="text-[14px] tracking-[0.07em] uppercase font-bold mt-0 mb-[8px] pb-[4px] border-b border-[#2f2f2f] text-[#f28e2b]">
                Feedback
            </h1>
            <div className="mt-[20px]">
                {loading && <p className="text-[#555] italic">Loading commemnts..</p>}
                {error && <p className="text-red-500 font-medium">Try later</p>}
                {!loading && !error && comments.map((comment, index) => (
                    <div
                        key={comment.id}
                        className={`bg-[#f9f9f9] border-l-4 border-[#f28e2b] p-[15px] mb-[15px] rounded-r-[8px] shadow-[0_2px_5px_rgba(0,0,0,0.05)] text-[#333] transition-colors dark:bg-[#333] dark:text-[#e0e0e0] dark:border-[#e15759]`}
                    >
                        <p className="mb-[8px]"><strong>Name:</strong> {comment.name}</p>
                        <p className="mb-[8px]">
                            <strong>Email:</strong>{" "}
                            <a href={`mailto:${comment.email}`} className="text-[#e15759] hover:underline transition-colors">
                                {comment.email}
                            </a>
                        </p>
                        <p className="m-0 leading-relaxed text-[15px]"><strong>Feedback:</strong> {comment.body}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default Reviews;
