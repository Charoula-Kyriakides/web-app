import { parse } from "node-html-parser";
import { Town } from "./towns";

export { Town };

/**
 * Fetch all the posts for a given town (group) on Freecycle
 * @param town Town
 */
export async function fetchPosts(town: Town): Promise<{
  group: {
    group_id: number;
    group_name: string;
    region_id: number;
    group_status_id: number;
    nga_approved: number;
    nga_approved_by: null;
    deleted: number;
    deleted_by: null;
    yahoo_group: number;
    invitation_only: number;
    num_members: number;
    num_posts_7day: number;
    nga_approved_date: null;
    description: string;
    max_other_groups: number;
    members_require_approval: number;
    max_wanteds_per_member: number;
    yahoo_group_name: string;
    default_tz: string;
    myfreecycle_optout: number;
    allow_image_posting: number;
    emergency_moderation: null;
    auto_mod_new_members: number;
    default_email_delivery: number;
    default_lang: string;
    latitude: number;
    longitude: number;
    treat_digest_responses_as_bounces: number;
    expire_wanteds_days: number;
    expire_offers_days: number;
    region: {
      region_id: number;
      region_name: string;
      country: { country_id: number; country_name: string };
    };
  };
  posts: {
    id: number;
    userId: number;
    subject: string;
    location: string;
    description: string;
    isApproved: 1 | 0;
    rejectReason: string | null;
    date: string;
    time: string;
    type: {
      typeId: number;
      const: "FC_POST_TAKEN" | "FC_POST_WANTED" | "FC_POST_OFFER";
      name: "TAKEN" | "WANTED" | "OFFER";
    };
    group: {
      id: number;
      name: string;
      uniqueName: Town;
      region: {
        id: number;
        name: string;
        country: {
          id: number;
          name: string;
        };
      };
      latitude: number;
      longitude: number;
      timezone: string;
    };
    static: null;
    image: string | null;
    thumb: string | null;
    images: string[] | null;
    thumbs: string[] | null;
    tags: [];
  }[];
  groups: {
    id: number;
    name: string;
    regionId: number;
    unqiueName: Town;
  }[];
  tags: {
    id: number;
    name: string;
    system: 1;
  }[];
  isMember: boolean;
  isPending: boolean;
  membershipLimitReached: boolean;
  supressAds: {
    side: boolean;
  };
}> {
  // Fetch the page with the data
  const res = await fetch(`https://www.freecycle.org/town/${town}`);
  const data = await res.text();
  const root = parse(data);

  // Find the specific element that they inject it into
  const dataEl = root.querySelector("fc-data");
  if (!dataEl)
    throw "Could not find the data element, Freecyle website may have changed.";

  // Find the attribute containing data and validate it is correct
  const rawData = dataEl.getAttribute("data");
  if (!rawData)
    throw "Could not find the raw post data, Freecycle website may have changed.";

  return JSON.parse(rawData);
}

/**
 * Fetch all the towns (groups) available on Freecycle
 * @returns Structured data
 */
export async function fetchTowns(): Promise<{
  groups: {
    name: string;
    uniqueName: string;
    latitude: number;
    longitude: number;
    regionId: number;
    region: {
      regionName: string;
      country: {
        name: string;
      };
    };
  }[];
  regions: {
    id: number;
    countryId: number;
  }[];
  memberships: null;
}> {
  // Fetch the page with the data
  const res = await fetch("https://www.freecycle.org/find-towns");
  const data = await res.text();
  const root = parse(data);

  // Find the specific element that they inject it into
  const dataEl = root.querySelector(".flex-video");
  if (!dataEl)
    throw "Could not find the data element, Freecyle website may have changed.";

  // Find the attribute containing data and validate it is correct
  const rawJS = dataEl.getAttribute("onload");
  const prefix = "$emit('loadTowns', ";
  const suffix = ")";
  if (!rawJS)
    throw "Could not find the town data load function, Freecycle website may have changed.";
  if (!rawJS.startsWith(prefix))
    throw "Freecycle website has changed, cannot parse.";
  if (!rawJS.endsWith(suffix))
    throw "Freecycle website has changed, cannot parse.";

  // Parse the data
  const rawData = rawJS.substring(prefix.length, rawJS.length - suffix.length);
  return JSON.parse(rawData);
}
