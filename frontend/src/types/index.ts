export interface PhrasalVerb {
  id: string;
  phrase: string;
  basePhrase: string;
  meaning: string;
  example: string;
  exampleOriginal: string;
  noteId: number;
  assets: Asset[];
}

export interface Asset {
  type: 'image' | 'video';
  url: string;
  created: string;
  prompt?: string;
  duration?: number;
  thumbnail?: string;
}
