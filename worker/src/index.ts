export interface Env {
  IMAGES: R2Bucket;
  METADATA: KVNamespace;
  CORS_ORIGIN: string;
}

// CORS 헤더
function corsHeaders(origin: string) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    const origin = env.CORS_ORIGIN || '*';

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders(origin) });
    }

    // 라우팅
    try {
      // GET /api/vocab - 전체 단어 목록
      if (path === '/api/vocab' || path === '/api/vocab/') {
        return await handleVocabList(env, origin);
      }

      // GET /api/vocab/:word - 특정 단어 메타데이터
      const vocabMatch = path.match(/^\/api\/vocab\/([a-zA-Z]+)$/);
      if (vocabMatch) {
        return await handleVocabDetail(env, vocabMatch[1], origin);
      }

      // GET /images/* - R2 이미지 서빙
      if (path.startsWith('/images/')) {
        return await handleImage(env, path.slice(8), origin);
      }

      // 404
      return new Response(JSON.stringify({ error: 'Not Found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
      });
    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
      });
    }
  },
};

// 전체 단어 목록
async function handleVocabList(env: Env, origin: string): Promise<Response> {
  const words = [
    'replenish', 'instigate', 'substantiate', 'deliberate', 'strenuous',
    'conjunction', 'extant', 'sedentary', 'invoke', 'pervasive'
  ];

  const vocabList = await Promise.all(
    words.map(async (word) => {
      const data = await env.METADATA.get(`vocab:${word}`, 'json');
      if (data) {
        const { images, scenarios_generated, ...summary } = data as any;
        return {
          ...summary,
          imageCount: images?.length || 0,
        };
      }
      return null;
    })
  );

  return new Response(JSON.stringify(vocabList.filter(Boolean)), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

// 특정 단어 상세
async function handleVocabDetail(env: Env, word: string, origin: string): Promise<Response> {
  const data = await env.METADATA.get(`vocab:${word.toLowerCase()}`, 'json');
  
  if (!data) {
    return new Response(JSON.stringify({ error: 'Word not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
    });
  }

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

// R2 이미지 서빙
async function handleImage(env: Env, key: string, origin: string): Promise<Response> {
  const object = await env.IMAGES.get(key);

  if (!object) {
    return new Response('Image not found', {
      status: 404,
      headers: corsHeaders(origin),
    });
  }

  const headers = new Headers();
  headers.set('Content-Type', object.httpMetadata?.contentType || 'image/png');
  headers.set('Cache-Control', 'public, max-age=31536000'); // 1년 캐시
  headers.set('ETag', object.httpEtag);
  
  // CORS
  Object.entries(corsHeaders(origin)).forEach(([k, v]) => headers.set(k, v));

  return new Response(object.body, { headers });
}
