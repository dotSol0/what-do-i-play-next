// Sample catalog. In production, replace with your indexed IMSLP dataset.
// Fields mirror the source CSV: Title, Composer, Instrumentation, Key,
// Piece Style (era), Average Duration, num_downloads, Permlink (url).
export const catalog = [
  { id: 0,  t: 'Cello Suite No.1 in G, BWV 1007',        c: 'Bach, J.S.',          inst: 'cello',               key: 'G major',  era: 'baroque',   dur: '18 min', dl: '41,208', form: 'suite',    url: 'https://imslp.org/wiki/Cello_Suite_No.1,_BWV_1007_(Bach,_Johann_Sebastian)' },
  { id: 1,  t: 'Cello Suite No.2 in D minor, BWV 1008',  c: 'Bach, J.S.',          inst: 'cello',               key: 'D minor',  era: 'baroque',   dur: '20 min', dl: '30,551', form: 'suite',    url: 'https://imslp.org/wiki/Cello_Suite_No.2,_BWV_1008_(Bach,_Johann_Sebastian)' },
  { id: 2,  t: 'Violin Partita No.2, BWV 1004',          c: 'Bach, J.S.',          inst: 'violin',              key: 'D minor',  era: 'baroque',   dur: '31 min', dl: '33,540', form: 'suite',    url: 'https://imslp.org/wiki/Violin_Partita_No.2,_BWV_1004_(Bach,_Johann_Sebastian)' },
  { id: 3,  t: 'Ricercari for Solo Cello',               c: 'Gabrielli, Domenico', inst: 'cello',               key: 'various',  era: 'baroque',   dur: '22 min', dl: '3,902',  form: 'suite',    url: 'https://imslp.org/wiki/7_Ricercari_(Gabrielli,_Domenico)' },
  { id: 4,  t: 'Sonata for Solo Cello, Op.8',            c: 'Kodály, Zoltán',      inst: 'cello',               key: 'B minor',  era: 'romantic',  dur: '28 min', dl: '9,114',  form: 'sonata',   url: 'https://imslp.org/wiki/Cello_Sonata,_Op.8_(Kod%C3%A1ly,_Zolt%C3%A1n)' },
  { id: 5,  t: 'Suite for Solo Cello No.3',              c: 'Reger, Max',          inst: 'cello',               key: 'C major',  era: 'romantic',  dur: '15 min', dl: '2,340',  form: 'suite',    url: 'https://imslp.org/wiki/3_Suites,_Op.131c_(Reger,_Max)' },
  { id: 6,  t: '34 Keyboard Sonatinas',                  c: 'Benda, Georg',        inst: 'piano or clavichord', key: 'various',  era: 'classical', dur: '—',      dl: '25,367', form: 'sonatina', url: 'https://imslp.org/wiki/34_Keyboard_Sonatinas_(Benda,_Georg)' },
  { id: 7,  t: 'Nocturne in E♭, Op.9 No.2',              c: 'Chopin, Frédéric',    inst: 'piano',               key: 'E♭ major', era: 'romantic',  dur: '4 min',  dl: '58,902', form: 'character',url: 'https://imslp.org/wiki/Nocturnes,_Op.9_(Chopin,_Fr%C3%A9d%C3%A9ric)' },
  { id: 8,  t: 'Gymnopédie No.1',                        c: 'Satie, Erik',         inst: 'piano',               key: 'D major',  era: 'romantic',  dur: '3 min',  dl: '64,771', form: 'character',url: 'https://imslp.org/wiki/Gymnop%C3%A9dies_(Satie,_Erik)' },
  { id: 9,  t: '34 Mazurkas',                            c: 'Wolff, Édouard',      inst: 'piano',               key: 'various',  era: 'romantic',  dur: '—',      dl: '72',     form: 'character',url: 'https://imslp.org/wiki/34_Mazurkas_(Wolff,_%C3%89douard)' },
  { id: 10, t: 'Prelude & Fugue in C, BWV 846',          c: 'Bach, J.S.',          inst: 'piano',               key: 'C major',  era: 'baroque',   dur: '5 min',  dl: '48,110', form: 'prelude',  url: 'https://imslp.org/wiki/Das_wohltemperierte_Klavier_I,_BWV_846-869_(Bach,_Johann_Sebastian)' },
  { id: 11, t: 'Songs Without Words, Op.19b',            c: 'Mendelssohn, Felix',  inst: 'piano',               key: 'various',  era: 'romantic',  dur: '20 min', dl: '21,400', form: 'character',url: 'https://imslp.org/wiki/Lieder_ohne_Worte,_Op.19b_(Mendelssohn,_Felix)' },
];

export const byId = (id) => catalog.find((p) => p.id === id) || catalog[0];
