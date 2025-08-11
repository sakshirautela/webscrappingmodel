import { useState } from "react";
import "./GetData.css";
import loaderGif from "./loading.gif";

export default function GetData() {
    const [data, setData] = useState(null);
    const [url, setUrl] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const fetchData = () => {
        if (!url) return;
        const encodedUrl = encodeURIComponent(url);
        setIsLoading(true);

        fetch(`${process.env.REACT_APP_API_BASE_URL}/api/data/${encodedUrl}`)
            .then(response => response.json())
            .then(result => {
                setData(result);
                setIsLoading(false);

            })
            .catch(error => {
                console.error("Error fetching data:", error);
                setData(null);
                setIsLoading(false);
            });
    };

    return (
        <div className="get-data-container">
            <h1>Data Fetching Component</h1>
            <input
                type="text"
                placeholder="Enter website URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={fetchData}>Scrape</button>

            {isLoading && (
                <div className="loader-container fade-in-out">
                    <div className="spinner"></div>
                </div>
            )}

            <div className="data-display">
                {data && (
                    <div>
                        <h2>Scraped Data:</h2>
                        {data.content && Array.isArray(data.content) && (
                            <div>
                                <h3>Content:</h3>
                                <ul>
                                    {data.content.map((item, index) => (
                                        <p key={index}>{item}</p>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
