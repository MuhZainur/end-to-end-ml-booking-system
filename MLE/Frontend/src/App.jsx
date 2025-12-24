import { useState } from 'react'
import axios from 'axios'

function App() {
    const [formData, setFormData] = useState({
        num_passengers: 1,
        sales_channel: 'Internet',
        trip_type: 'RoundTrip',
        purchase_lead: 30,
        length_of_stay: 5,
        flight_hour: 12,
        flight_day: 'Mon',
        route: 'AKLDEL',
        booking_origin: 'New Zealand',
        wants_extra_baggage: true,
        wants_preferred_seat: false,
        wants_in_flight_meals: true,
        flight_duration: 8.5
    })

    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        // Format payload to match Backend Schema (ints and 1/0 for bools)
        const payload = {
            ...formData,
            num_passengers: parseInt(formData.num_passengers),
            purchase_lead: parseInt(formData.purchase_lead),
            length_of_stay: parseInt(formData.length_of_stay),
            flight_hour: parseInt(formData.flight_hour),
            flight_duration: parseFloat(formData.flight_duration),
            wants_extra_baggage: formData.wants_extra_baggage ? 1 : 0,
            wants_preferred_seat: formData.wants_preferred_seat ? 1 : 0,
            wants_in_flight_meals: formData.wants_in_flight_meals ? 1 : 0,
            // Uppercase Route
            route: formData.route.toUpperCase()
        }

        try {
            // Priority: Env Var (if built with it) > Production URL > Localhost
            const API_URL = import.meta.env.VITE_API_URL || "https://ba-backend-567427950134.us-central1.run.app";
            console.log("Using API URL:", API_URL); // Debugging

            const response = await axios.post(`${API_URL}/predict`, payload)
            setResult(response.data)
        } catch (err) {
            setError('Connection Error: Is the FastAPI Backend running?')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
            {/* Header */}
            <header className="bg-[#002244] text-white p-6 shadow-lg">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">British Airways</h1>
                        <p className="text-sm text-slate-300">Customer Booking Predictor</p>
                    </div>
                    <div className="text-4xl">✈️</div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto p-6">
                <div className="grid md:grid-cols-2 gap-8">

                    {/* Input Form */}
                    <div className="bg-white p-6 rounded-xl shadow-md border border-slate-100">
                        <h2 className="text-xl font-bold mb-6 text-[#002244] border-b pb-2">Passenger Details</h2>

                        <form onSubmit={handleSubmit} className="space-y-4">

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Route (Code)</label>
                                    <input name="route" value={formData.route} onChange={handleChange}
                                        className="w-full p-2 border rounded focus:ring-2 focus:ring-[#D71920] outline-none uppercase" />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Origin Country</label>
                                    <input name="booking_origin" value={formData.booking_origin} onChange={handleChange}
                                        className="w-full p-2 border rounded focus:ring-2 focus:ring-[#D71920] outline-none" />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Flight Day</label>
                                    <select name="flight_day" value={formData.flight_day} onChange={handleChange} className="w-full p-2 border rounded">
                                        {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(d => <option key={d} value={d}>{d}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Flight Hour</label>
                                    <input type="number" name="flight_hour" value={formData.flight_hour} onChange={handleChange}
                                        min="0" max="23" className="w-full p-2 border rounded" />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Passengers</label>
                                    <input type="number" name="num_passengers" value={formData.num_passengers} onChange={handleChange}
                                        min="1" className="w-full p-2 border rounded" />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Sales Channel</label>
                                    <select name="sales_channel" value={formData.sales_channel} onChange={handleChange} className="w-full p-2 border rounded">
                                        <option value="Internet">Internet</option>
                                        <option value="Mobile">Mobile</option>
                                    </select>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Purchase Lead (Days)</label>
                                    <input type="number" name="purchase_lead" value={formData.purchase_lead} onChange={handleChange}
                                        className="w-full p-2 border rounded" />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1">Stay Length (Days)</label>
                                    <input type="number" name="length_of_stay" value={formData.length_of_stay} onChange={handleChange}
                                        className="w-full p-2 border rounded" />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold mb-1">Flight Duration (Hours)</label>
                                <input type="number" name="flight_duration" value={formData.flight_duration} onChange={handleChange}
                                    step="0.1" className="w-full p-2 border rounded" />
                            </div>

                            <div className="bg-slate-50 p-4 rounded-lg space-y-2">
                                <label className="flex items-center space-x-2 cursor-pointer">
                                    <input type="checkbox" name="wants_extra_baggage" checked={formData.wants_extra_baggage} onChange={handleChange} className="w-4 h-4 text-[#D71920]" />
                                    <span className="text-sm">Extra Baggage</span>
                                </label>
                                <label className="flex items-center space-x-2 cursor-pointer">
                                    <input type="checkbox" name="wants_in_flight_meals" checked={formData.wants_in_flight_meals} onChange={handleChange} className="w-4 h-4 text-[#D71920]" />
                                    <span className="text-sm">In-Flight Meals</span>
                                </label>
                                <label className="flex items-center space-x-2 cursor-pointer">
                                    <input type="checkbox" name="wants_preferred_seat" checked={formData.wants_preferred_seat} onChange={handleChange} className="w-4 h-4 text-[#D71920]" />
                                    <span className="text-sm">Preferred Seat</span>
                                </label>
                            </div>

                            <button type="submit" disabled={loading}
                                className="w-full bg-[#D71920] hover:bg-red-700 text-white font-bold py-3 rounded-lg transition-colors flex justify-center items-center">
                                {loading ? (
                                    <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></span>
                                ) : 'Predict Booking Probability'}
                            </button>

                        </form>
                    </div>

                    {/* Result Section */}
                    <div className="space-y-6">
                        <div className="bg-[#002244] text-white p-6 rounded-xl shadow-lg h-full flex flex-col justify-center items-center text-center">
                            {!result && !error && (
                                <>
                                    <div className="text-6xl mb-4">✈️</div>
                                    <h3 className="text-xl font-light opacity-80">Ready to Analyze</h3>
                                    <p className="text-sm opacity-60 mt-2">Fill the form to see AI predictions.</p>
                                </>
                            )}

                            {loading && (
                                <div className="animate-pulse">
                                    <div className="h-4 bg-blue-400 rounded w-32 mb-4"></div>
                                    <div className="h-4 bg-blue-400 rounded w-48"></div>
                                </div>
                            )}

                            {error && (
                                <div className="bg-red-500/20 border border-red-500 text-red-100 p-4 rounded-lg">
                                    {error}
                                </div>
                            )}

                            {result && (
                                <div className="animate-fade-in-up w-full">
                                    <p className="text-sm uppercase tracking-widest opacity-70 mb-2">Prediction Result</p>

                                    {result.prediction === 1 ? (
                                        <div className="bg-green-500 text-white p-4 rounded-lg mb-4 shadow-inner">
                                            <h2 className="text-3xl font-bold">Booking Likely</h2>
                                        </div>
                                    ) : (
                                        <div className="bg-slate-600 text-white p-4 rounded-lg mb-4 shadow-inner">
                                            <h2 className="text-3xl font-bold">Booking Unlikely</h2>
                                        </div>
                                    )}

                                    <div className="grid grid-cols-2 gap-4 mt-6 text-left">
                                        <div className="bg-white/10 p-3 rounded">
                                            <span className="block text-xs opacity-60">Confidence Score</span>
                                            <span className="text-2xl font-mono text-[#D71920] font-bold">
                                                {(result.confidence_score * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                        <div className="bg-white/10 p-3 rounded">
                                            <span className="block text-xs opacity-60">Model Logic</span>
                                            <span className="text-sm">{result.message}</span>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </main>
        </div>
    )
}

export default App
