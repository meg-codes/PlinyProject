import { DetailedPerson } from '../../people-detail'
export const tacitus:DetailedPerson = {
  id: 1,
  letters_to: [
      "1.6",
      "1.20",
      "4.13",
      "6.9",
      "6.16",
      "6.20",
      "7.20",
      "7.33",
      "8.7",
      "9.10",
      "9.14"
  ],
  citations: [
      "A.N. Sherwin-White, <em>The Letters of Pliny: A Social and Historical Commentary</em> (Oxford: Clarendon, 1966), 99-100.",
      "Anthony R. Birley, <em>An Onomasticon to the Younger Pliny: <em>Letters</em> and <em>Panegryic</em></em> (Leipzig: K G Saur, 2000), 53.",
      "G. Alföldy, \"Bricht der Schweigsame sein Schweigen?,\" <em>Mitteilungen des Deutschen Archäologischen Instituts, Römische Abteilung</em> 102 (1995): 251-268.",
      "Anthony R. Birley, \"The life and death of Cornelius Tacitus,\" <em>Historia</em> 49 (2000): 230-247."
  ],
  gender: "Male",
  citizen: "Yes",
  equestrian: "No",
  senatorial: "Yes",
  consular: "Yes",
  nomina: "Cornelius Tacitus",
  birth: null,
  death: null,
  cos: null,
  cos_suff: 97,
  floruit: null,
  certainty_of_id: 5,
  notes: "",
  from_comum: false,
  mentioned_in: [],
  related_to: []
};

const tacitusCopy: DetailedPerson = Object.assign({}, tacitus);

tacitusCopy.birth = 60;
tacitusCopy.death = 96;
tacitusCopy.cos = 78;
tacitusCopy.floruit = 70;
export const fakeDatesTacitus = tacitusCopy;



