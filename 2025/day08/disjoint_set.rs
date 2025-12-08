// https://gist.github.com/orez-/eeca93b20d10343e17f7cd93e833dc61
use std::collections::HashMap;
use std::hash;

pub(crate) struct DisjointSet<T> {
    elements: HashMap<T, usize>,
    parents: HashMap<usize, usize>,
}

impl<T: Eq + hash::Hash> DisjointSet<T> {
    pub fn new() -> Self {
        Self {
            elements: HashMap::new(),
            parents: HashMap::new(),
        }
    }

    pub fn insert(&mut self, item: T) -> usize {
        if let Some(&id) = self.elements.get(&item) {
            self.find_root(id)
        } else {
            let id = self.elements.len();
            self.elements.insert(item, id);
            id
        }
    }

    fn find_root(&mut self, id: usize) -> usize {
        let mut node = id;
        while let Some(&parent) = self.parents.get(&node) {
            node = parent;
        }
        let parent = node;

        node = id;
        while let Some(&old_parent) = self.parents.get(&node) {
            self.parents.insert(node, parent);
            node = old_parent;
        }
        parent
    }

    pub fn merge(&mut self, item1: T, item2: T) -> bool {
        let group1 = self.insert(item1);
        let group2 = self.insert(item2);

        if group1 == group2 { return false; }
        self.parents.insert(group1, group2);
        true
    }

    pub fn into_groups(mut self) -> impl Iterator<Item = Vec<T>> {
        let mut groups = HashMap::new();
        let elements = std::mem::take(&mut self.elements);
        for (item, id) in elements {
            let root_id = self.find_root(id);
            groups.entry(root_id).or_insert_with(Vec::new).push(item);
        }
        groups.into_values()
    }
}
