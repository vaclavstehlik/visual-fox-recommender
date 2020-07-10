class DatasetAnalysisResult:
    _numeric = None
    _categoric = None
    _mixed_categoric_numeric = None
    _geospatial = None
    _temporal = None
    _one_ts = None
    _multiple_ts = None
    _negative_values = None

    @property
    def numeric(self):
        return self._categoric

    @property
    def categoric(self):
        return self._numeric

    @property
    def mixed_categoric_numeric(self):
        return self._mixed_categoric_numeric

    @property
    def geospatial(self):
        return self._geospatial

    @property
    def temporal(self):
        return self._temporal

    @property
    def one_ts(self):
        return self._one_ts

    @property
    def multiple_ts(self):
        return self._multiple_ts

    @property
    def negative_values(self):
        return self._negative_values

    @numeric.setter
    def numeric(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._numeric = value

    @categoric.setter
    def categoric(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._categoric = value

    @mixed_categoric_numeric.setter
    def mixed_categoric_numeric(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._mixed_categoric_numeric = value

    @geospatial.setter
    def geospatial(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._geospatial = value

    @temporal.setter
    def temporal(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._temporal = value

    @one_ts.setter
    def one_ts(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._one_ts = value

    @multiple_ts.setter
    def multiple_ts(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._multiple_ts = value

    @negative_values.setter
    def negative_values(self, value):
        if type(value) is not bool:
            raise TypeError("name must be a bool")
        self._negative_values = value
