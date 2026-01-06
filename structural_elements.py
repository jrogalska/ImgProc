import numpy as np

STRUCT_ELEMENTS = {
    "i": {
        "shape": np.array([
            [1,1]
            ], dtype=np.uint8),
        "origin": (0, 0)
    },

    "ii": {
        "shape": np.array([
            [1],
            [1]
            ], dtype=np.uint8),
        "origin": (0, 0)
    },

    "iii": {
        "shape": np.array([
            [1,1,1],
            [1,1,1],
            [1,1,1]
            ], dtype=np.uint8),
        "origin": (1, 1)
    },

    "iv": {
        "shape": np.array([
            [0,1,0],
            [1,1,1],
            [0,1,0]
            ], dtype=np.uint8),
        "origin": (1,1)
    },

    "v": {
        "shape": np.array([
            [1,1],
            [1,0]
            ], dtype=np.uint8),
        "origin": (0,0)
    },

    "vi": {
        "shape": np.array([
            [0,1],
            [1,0]
            ], dtype=np.uint8),
        "origin": (0,0)
    },    

    "vii": {
        "shape": np.array([
            [1,1,1]
            ], dtype=np.uint8),
        "origin": (0,1)
    },  

    "viii": {
        "shape": np.array([
            [1,0,1]
            ], dtype=np.uint8),
        "origin": (0,1)
    },  

    "ix": {
        "shape": np.array([
            [1,1],
            [1,0]
            ], dtype=np.uint8),
        "origin": (0,1)
    },  

    "x": {
        "shape": np.array([
            [1,1],
            [1,0]
            ], dtype=np.uint8),
        "origin": (1,0)
    },  

    "xi[1]": {
        "shape": np.array([
            [1,-1,-1],
            [1,0,-1],
            [1,-1,-1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xi[2]": {
        "shape": np.array([
            [1,1,1],
            [-1,0,-1],
            [-1,-1,-1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xi[3]": {
        "shape": np.array([
            [-1,-1,1],
            [-1,0,1],
            [-1,-1,1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xi[4]": {
        "shape": np.array([
            [-1,-1,-1],
            [-1,0,-1],
            [1,1,1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xv": {
        "shape": np.array([
            [0,0,1],
            [1,0,1],
            [1,0,1]
        ], dtype=np.int8),
        "origin": (1,1)
    },

    "xii[1]": {
        "shape": np.array([
            [0,0,0],
            [-1,1,-1],
            [1,1,1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[2]": {
        "shape": np.array([
            [-1,0,0],
            [1,1,0],
            [1,1,-1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[3]": {
        "shape": np.array([
            [1,-1,0],
            [1,1,0],
            [1,-1,0]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[4]": {
        "shape": np.array([
            [1,1,-1],
            [1,1,0],
            [-1,0,0]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[5]": {
        "shape": np.array([
            [1,1,1],
            [-1,1,-1],
            [0,0,0]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[6]": {
        "shape": np.array([
            [-1,1,1],
            [0,1,1],
            [0,0,-1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[7]": {
        "shape": np.array([
            [0,-1,1],
            [0,1,1],
            [0,-1,1]
            ], dtype=np.int8),
        "origin": (1,1)
        },
    "xii[8]": {
        "shape": np.array([
            [0,0,-1],
            [0,1,1],
            [-1,1,1]
            ], dtype=np.int8),
        "origin": (1,1)
        }
}