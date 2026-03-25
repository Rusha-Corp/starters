import { http, HttpResponse, delay } from 'msw';

export interface HealthResponse {
  status: string;
  version: string;
  db?: string;
}

export interface Item {
  id: number;
  name: string;
  description: string;
  created_at?: string;
  updated_at?: string;
}

export interface ItemListResponse {
  items: Item[];
  total: number;
}

// In-memory store for mock data
let items: Item[] = [
  { id: 1, name: 'Sample Item', description: 'This is a sample item for testing' },
];
let nextId = 2;

export const handlers = [
  // Health endpoints
  http.get('/health', async () => {
    await delay(100);
    return HttpResponse.json<HealthResponse>({
      status: 'ok',
      version: '0.1.0',
      db: 'connected',
    });
  }),

  http.get('/health/live', async () => {
    await delay(50);
    return HttpResponse.json<HealthResponse>({
      status: 'ok',
      version: '0.1.0',
    });
  }),

  http.get('/health/ready', async () => {
    await delay(100);
    return HttpResponse.json<HealthResponse>({
      status: 'ready',
      version: '0.1.0',
      db: 'connected',
    });
  }),

  // Items endpoints
  http.get('/api/items', async () => {
    await delay(100);
    return HttpResponse.json<ItemListResponse>({
      items,
      total: items.length,
    });
  }),

  http.post('/api/items', async ({ request }) => {
    await delay(200);
    const body = (await request.json()) as { name: string; description: string };
    const newItem: Item = {
      id: nextId++,
      name: body.name,
      description: body.description,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    items.push(newItem);
    return HttpResponse.json(newItem, { status: 201 });
  }),

  http.get('/api/items/:id', async ({ params }) => {
    await delay(100);
    const id = parseInt(params.id as string, 10);
    const item = items.find((i) => i.id === id);
    if (!item) {
      return HttpResponse.json({ detail: 'Item not found' }, { status: 404 });
    }
    return HttpResponse.json(item);
  }),

  http.delete('/api/items/:id', async ({ params }) => {
    await delay(100);
    const id = parseInt(params.id as string, 10);
    const index = items.findIndex((i) => i.id === id);
    if (index === -1) {
      return HttpResponse.json({ detail: 'Item not found' }, { status: 404 });
    }
    items.splice(index, 1);
    return new HttpResponse(null, { status: 204 });
  }),
];
