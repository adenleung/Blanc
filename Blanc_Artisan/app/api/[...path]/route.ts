import {env} from 'cloudflare:workers';
import {handleCommerce} from '../../../lib/commerce.mjs';
export const dynamic='force-dynamic';
export async function GET(request:Request){return handleCommerce(request,env)}
export async function POST(request:Request){return handleCommerce(request,env)}
