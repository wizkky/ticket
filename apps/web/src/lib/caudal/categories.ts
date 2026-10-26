import * as m from '$lib/paraglide/messages.js';

/** Editorial categories use the existing public tag filter; no inferred affiliations. */
export const CATEGORY_TAGS = {
	musica: ['música', 'concierto', 'dj'],
	escena: ['artes escénicas', 'danza', 'teatro', 'cine', 'audiovisual'],
	oficios: ['taller', 'oficios', 'artesanía'],
	formacion: ['curso', 'formación', 'charla'],
	movimiento: ['deporte', 'movimiento', 'yoga'],
	bienestar: ['bienestar', 'terapias', 'salud'],
	naturaleza: ['naturaleza', 'experiencias', 'aire libre'],
	comunidad: ['comunidad', 'encuentro', 'actividad comunitaria']
} as const;

export type ActivityCategory = keyof typeof CATEGORY_TAGS;

export function parseCategory(value: string | null | undefined): ActivityCategory | undefined {
	return value && Object.hasOwn(CATEGORY_TAGS, value) ? (value as ActivityCategory) : undefined;
}

export function categoryTags(
	category: ActivityCategory | undefined,
	tags?: string[]
): string[] | undefined {
	return category ? [...CATEGORY_TAGS[category]] : tags;
}

/** Static message calls let the production build keep translations route-sized. */
export function activityCategories() {
	return [
		{ id: 'musica', label: m['creative.music']() },
		{ id: 'escena', label: m['creative.arts']() },
		{ id: 'oficios', label: m['creative.crafts']() },
		{ id: 'formacion', label: m['creative.learning']() },
		{ id: 'movimiento', label: m['creative.movement']() },
		{ id: 'bienestar', label: m['creative.wellbeing']() },
		{ id: 'naturaleza', label: m['creative.nature']() },
		{ id: 'comunidad', label: m['creative.communityCategory']() }
	] as const;
}
