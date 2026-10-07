import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata={title:'Blanc Artisan — Flowers that say it beautifully',description:'Handcrafted bouquets and floral gifts in Singapore.'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><head><link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet"/></head><body><noscript><p style={{padding:"20px"}}>Please enable JavaScript to select bouquet options, use the cart and pay. You can also contact our florist on +65 8580 9956.</p></noscript>{children}</body></html>}
