using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace BjSTools.File
{
    public class BjSJsonObject : IEnumerable<BjSJsonObjectMember>
    {
        private List<BjSJsonObjectMember> Members { get; set; }

        public BjSJsonObject()
        {
            Members = new List<BjSJsonObjectMember>();
        }

        public BjSJsonObject(string data) : this()
        {
            BjSJsonObject obj = BjSJsonHelper.BjSJsonReader.Parse(data).FirstOrDefault(o => o is BjSJsonObject) as BjSJsonObject;
            if (obj != null) this.Members = obj.Members;
        }

        public BjSJsonObject(string filename, Encoding fileEncoding) : this()
        {
            if (fileEncoding == null) fileEncoding = Encoding.Default;

            using (StreamReader s = new StreamReader(filename, fileEncoding))
            {
                BjSJsonObject obj = BjSJsonHelper.BjSJsonReader.Parse(s).FirstOrDefault(o => o is BjSJsonObject) as BjSJsonObject;
                if (obj != null) this.Members = obj.Members;
            }
        }

        public BjSJsonObject(StreamReader stream) : this()
        {
            BjSJsonObject obj = BjSJsonHelper.BjSJsonReader.Parse(stream).FirstOrDefault(o => o is BjSJsonObject) as BjSJsonObject;
            if (obj != null) this.Members = obj.Members;
        }

        public override string ToString()
        {
            return String.Format("Object[{0}]", this.Members.Count);
        }


        public string ToJsonString(bool compressed)
        {
            return this.ToJsonString(compressed, 0);
        }
        internal string ToJsonString(bool compressed, int level)
        {
            if (compressed)
                return String.Format("{{{0}}}", String.Join(",", Members.Select(m => m.ToJsonString(true, 0)).ToArray()));
            else if (this.Members.Count == 0)
                return "{ }";
            else
            {
                string levelStr = BjSJsonHelper.GetLevelString(level);
                string level1 = BjSJsonHelper.GetLevelString(level + 1);
                return String.Format("{{\r\n{0}{2}\r\n{1}}}", level1, levelStr, String.Join(String.Format(",\r\n{0}", level1), 
                    Members.Select(m => m.ToJsonString(false, level + 1)).ToArray()));
            }
        }

        #region Enumerator & other public member access

        public IEnumerator<BjSJsonObjectMember> GetEnumerator() { return this.Members.GetEnumerator(); }

        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()
        {
            return this.Members.GetEnumerator();
        }


        public BjSJsonValueKind GetValueKind(int index)
        {
            return BjSJsonHelper.GetValueKind(this.Members[index].Value);
        }


        public int Count { get { return this.Members.Count; } }

        public void Add(string name, object value)
        {
            if (value == null || value is BjSJsonObject || value is BjSJsonArray || value is string || value is decimal || value is bool)
                this.Members.Add(new BjSJsonObjectMember { Name = name, Value = value });
            else
                throw new ArgumentException("The value must be a BjSJsonObject, BjSJsonArray, String, Decimal, Boolean or null!", "value");
        }

        public void Add(BjSJsonObjectMember item)
        {
            if (item == null) throw new NullReferenceException("A BjSJsonObjectMember must not be null when added!");

            this.Members.Add(item);
        }


        public void RemoveAt(int index) { this.Members.RemoveAt(index); }


        public int Remove(string name) { return this.Members.RemoveAll(m => m.Name.Equals(name)); }

        public int Remove(BjSJsonObjectMember item) { return this.Members.RemoveAll(m => m.Equals(item)); }


        public BjSJsonObjectMember this[int index]
        {
            get { return Members[index]; }
            set 
            {
                if (value == null) throw new NullReferenceException();
                Members[index] = value;
            }
        }


        public object this[string name]
        {
            get
            {
                BjSJsonObjectMember member = this.Members.FirstOrDefault(m => m.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
                if (member == null) return null;
                else return member.Value;
            }
            set
            {
                if (!(value == null || value is BjSJsonObject || value is BjSJsonArray || value is string || value is decimal || value is bool))
                    throw new ArgumentException("The value must be a BjSJsonObject, BjSJsonArray, String, Decimal, Boolean or null!", "value");

                BjSJsonObjectMember member = this.Members.FirstOrDefault(m => m.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
                if (member == null) this.Members.Add(new BjSJsonObjectMember(name, value));
                else member.Value = value;
            }
        }

        #endregion

    }

    public class BjSJsonArray : IEnumerable<object>
    {
        private List<object> Values { get; set; }

        public BjSJsonArray()
        {
            Values = new List<object>();
        }

        public BjSJsonArray(params object[] values) : this()
        {
            if (values == null || values.Length == 0) return;
            foreach (object obj in values) { this.Add(obj); }
        }

        public override string ToString() { return String.Format("Array[{0}]", this.Values.Count); }

        internal string ToJsonString(bool compressed, int level)
        {
            if (compressed)
                return String.Format("[{0}]", String.Join(",", this.Values.Select(v => BjSJsonHelper.ToJsonString(v, true, 0)).ToArray()));
            else if (this.Values.Count == 0)
                return "[ ]";
            else
            {
                string levelStr = BjSJsonHelper.GetLevelString(level);
                string level1 = BjSJsonHelper.GetLevelString(level + 1);
                return String.Format("[\r\n{0}{2}\r\n{1}]", level1, levelStr, String.Join(String.Format(",\r\n{0}", level1),
                    this.Values.Select(v => BjSJsonHelper.ToJsonString(v, false, level + 1)).ToArray()));
            }
        }

        #region Enumerator & other public values access

        public IEnumerator<object> GetEnumerator()
        {
            return this.Values.GetEnumerator();
        }

        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()
        {
            return this.Values.GetEnumerator();
        }

        public BjSJsonValueKind GetValueKind(int index)
        {
            return BjSJsonHelper.GetValueKind(this.Values[index]);
        }


        public int Count { get { return this.Values.Count; } }

        public object this[int index]
        {
            get { return Values[index]; }
            set
            {
                if (!(value == null || value is BjSJsonObject || value is BjSJsonArray || value is string || value is decimal || value is bool))
                    throw new ArgumentException("The value must be a BjSJsonObject, BjSJsonArray, String, Decimal, Boolean or null!", "value");

                Values[index] = value;
            }
        }

        public void Add(object value)
        {
            if (!(value == null || value is BjSJsonObject || value is BjSJsonArray || value is string || value is decimal || value is bool))
                throw new ArgumentException("The value must be a BjSJsonObject, BjSJsonArray, String, Decimal, Boolean or null!", "value");

            this.Values.Add(value);
        }

        public bool Remove(object value) { return this.Values.Remove(value); }

        public void RemoveAt(int index) { this.Values.RemoveAt(index); }

        #endregion
    }

    public class BjSJsonObjectMember
    {
        public string Name { get; set; }

        private object _value = null;

        public object Value
        {
            get { return _value; }
            set
            {
                if (!(value == null || value is BjSJsonObject || value is BjSJsonArray || value is string || value is decimal || value is bool))
                    throw new ArgumentException("The value must be a BjSJsonObject, BjSJsonArray, String, Decimal, Boolean or null!", "value");

                _value = value;
            }
        }

        public BjSJsonObjectMember() { }

        public BjSJsonObjectMember(string name, object value)
        {
            this.Name = name;
            this.Value = value;
        }


        public BjSJsonValueKind ValueKind { get { return BjSJsonHelper.GetValueKind(this.Value); } }

        public override string ToString()
        {
            return String.Format("{0} : {1}", this.Name, BjSJsonHelper.GetValueDisplayString(this.Value));
        }

        internal string ToJsonString(bool compressed, int level)
        {
            if (compressed)
                return String.Format("\"{0}\":{1}", BjSJsonHelper.EscapeString(this.Name), BjSJsonHelper.ToJsonString(this.Value, true, 0));
            else
                return String.Format("\"{0}\" : {1}", BjSJsonHelper.EscapeString(this.Name), BjSJsonHelper.ToJsonString(this.Value, false, level + 1));
        }
    }

    public enum BjSJsonValueKind
    {
        Object,
        Array,
        String,
        Number,
        Boolean,
        Null
    }

    public static class BjSJsonHelper
    {
        #region Reader state machine

        internal class BjSJsonReader
        {
            private ReaderState State;

            internal BjSJsonReader() { }

            public static List<object> Parse(string data)
            {
                BjSJsonReader reader = new BjSJsonReader();
                StartState start = new StartState(reader);

                reader.State = start;

                foreach (char c in data)
                    reader.State.Process(c);

                return start.Objects;
            }
            public static List<object> Parse(StreamReader s)
            {
                BjSJsonReader reader = new BjSJsonReader();
                StartState start = new StartState(reader);

                reader.State = start;

                char[] buffer = new char[8192];
                int len;
                while (!s.EndOfStream)
                {
                    len = s.ReadBlock(buffer, 0, buffer.Length);
                    for (int i = 0; i < len; i++)
                        reader.State.Process(buffer[i]);
                }
                return start.Objects;
            }

            #region States

            private abstract class ReaderState
            {
                protected BjSJsonReader _reader;
                protected ReaderState _previous;
                public abstract void Process(char c);
            }
            private class StartState : ReaderState
            {
                public List<object> Objects { get; private set; }

                public StartState(BjSJsonReader reader)
                {
                    _reader = reader;
                    Objects = new List<object>();
                }

                public override void Process(char c)
                {
                    _reader.State = new SelectValueState(_reader, this, obj =>
                    {
                        _reader.State = this;
                        Objects.Add(obj);
                    });
                    _reader.State.Process(c);
                }
            }

            private class SelectValueState : ReaderState
            {
                private Action<object> _onDone;

                public SelectValueState(BjSJsonReader reader, ReaderState previous, Action<object> onDone)
                {
                    _reader = reader;
                    _previous = previous;
                    _onDone = onDone;
                }
                public override void Process(char c)
                {
                    if (c == '{') // Object
                        _reader.State = new ObjectState(_reader, obj => _onDone(obj));
                    else if (c == '[') // Array
                        _reader.State = new ArrayStartState(_reader, arr => _onDone(arr));
                    else if ("-0123456789.".Contains(c)) // Number
                    {
                        _reader.State = new CaptureNumberState((d, lc) =>
                        {
                            _onDone(d);
                            _reader.State.Process(lc);
                        });
                        _reader.State.Process(c);
                    }
                    else if (c == '"') // String
                        _reader.State = new CaptureStringState(s => _onDone(s));
                    else if (c == 't' || c == 'T') // true
                        _reader.State = new CaptureExactState("true", () => _onDone(true));
                    else if (c == 'f' || c == 'F') // false
                        _reader.State = new CaptureExactState("false", () => _onDone(false));
                    else if (c == 'n' || c == 'N') // null
                        _reader.State = new CaptureExactState("null", () => _onDone(null));
                    else if (c == ']' || c == '}')
                    {
                        _reader.State = _previous;
                        _reader.State.Process(c);
                    }
                }
            }

            private class CaptureStringState : ReaderState
            {
                private Action<string> _onDone;
                private StringBuilder _buffer;
                private int _unicodeCount;
                private int _unicodeValue;
                private bool _inEscape;

                public CaptureStringState(Action<string> onDone)
                {
                    _onDone = onDone;
                    _buffer = new StringBuilder();
                    _inEscape = false;
                }

                public override void Process(char c)
                {
                    if (_inEscape)
                    {
                        _inEscape = false;
                        #region Escapes
                        if (c == '"' || c == '/' || c == '\\') _buffer.Append(c);
                        else if (c == 'b') _buffer.Append('\b');
                        else if (c == 'f') _buffer.Append('\f');
                        else if (c == 'n') _buffer.Append('\n');
                        else if (c == 'r') _buffer.Append('\r');
                        else if (c == 't') _buffer.Append('\t');
                        else if (c == 'u' && _unicodeCount == 0)
                        {
                            _unicodeCount++;
                            _unicodeValue = 0;
                            _inEscape = true;
                        }
                        else if (_unicodeCount != 0 && "0123456789ABCDEFabcdef".Contains(c))
                        {
                            int digit = "0123456789ABCDEF".IndexOf(c.ToString().ToUpper()[0]);
                            _unicodeValue = (_unicodeValue << 8) | digit;
                            _unicodeCount++;
                            if (_unicodeCount == 5)
                                _buffer.Append((char)_unicodeValue);
                            else
                                _inEscape = true;
                        }
                        else if (_unicodeCount > 1)
                        {
                            _buffer.Append((char)_unicodeValue);
                            _buffer.Append(c);
                        }
                        else
                            _buffer.Append(c);
                        #endregion
                    }
                    else if (c == '\\')
                    {
                        _inEscape = true;
                        _unicodeCount = 0;
                    }
                    else if (c == '"')
                        _onDone(_buffer.ToString());
                    else
                        _buffer.Append(c);
                }
            }
            private class CaptureNumberState : ReaderState
            {
                private Action<decimal, char> _onDone;
                private StringBuilder _buffer;

                public CaptureNumberState(Action<decimal, char> onDone)
                {
                    _onDone = onDone;
                    _buffer = new StringBuilder();
                }

                public override void Process(char c)
                {
                    if ("-+0123456789.eE".Contains(c))
                        _buffer.Append(c);
                    else
                    {
                        decimal d = 0m;
                        try { d = Decimal.Parse(_buffer.ToString().ToUpper(), System.Globalization.CultureInfo.InvariantCulture.NumberFormat); }
                        catch { }
                        _onDone(d, c);
                    }
                }
            }
            private class CaptureExactState : ReaderState
            {
                private Action _onDone;
                private string _what;
                private int _pos;

                public CaptureExactState(string whatToRead, Action onDone)
                {
                    _onDone = onDone;
                    _what = whatToRead;
                    _pos = 1;
                }

                public override void Process(char c)
                {
                    if (_what[_pos] == c.ToString().ToLower()[0])
                        _pos++;
                    else
                        throw new FormatException("Unexpected value found!");

                    if (_pos == _what.Length)
                        _onDone();
                }
            }

            private class ObjectState : ReaderState
            {
                private Action<BjSJsonObject> _onDone;
                private BjSJsonObject _curr;
                private BjSJsonObjectMember _currSubVal;
                private enum InternalState { WaitForName, WaitForSeperator, WaitForNextOrEnd }
                private InternalState _internState;

                public ObjectState(BjSJsonReader reader, Action<BjSJsonObject> onDone)
                {
                    _reader = reader;
                    _onDone = onDone;
                    _curr = new BjSJsonObject();
                    _internState = InternalState.WaitForName;
                }
                public override void Process(char c)
                {
                    if (c == '}') // End of Object
                    {
                        _onDone(_curr);
                    }
                    else if (_internState == InternalState.WaitForName)
                    {
                        if (c == '"')
                        {
                            _reader.State = new CaptureStringState(name =>
                            {
                                _reader.State = this;

                                _currSubVal = new BjSJsonObjectMember();
                                _currSubVal.Name = name;
                                _curr.Add(_currSubVal);

                                _internState = InternalState.WaitForSeperator;
                            });
                        }
                    }
                    else if (_internState == InternalState.WaitForSeperator)
                    {
                        if (c == ':')
                        {
                            _reader.State = new SelectValueState(_reader, this, obj =>
                            {
                                _currSubVal.Value = obj;
                                _reader.State = this;
                                _internState = InternalState.WaitForNextOrEnd;
                            });
                        }
                    }
                    else if (_internState == InternalState.WaitForNextOrEnd)
                    {
                        if (c == ',')
                            _internState = InternalState.WaitForName;
                    }
                }
            }

            private class ArrayStartState : ReaderState
            {
                private Action<BjSJsonArray> _onDone;
                private BjSJsonArray _curr;
                private bool _waitForSeperator;

                public ArrayStartState(BjSJsonReader reader, Action<BjSJsonArray> onDone)
                {
                    _reader = reader;
                    _onDone = onDone;
                    _curr = new BjSJsonArray();
                    _waitForSeperator = false;
                }

                public override void Process(char c)
                {
                    if (c == ']')
                        _onDone(_curr);
                    else if (!_waitForSeperator)
                    {
                        _reader.State = new SelectValueState(_reader, this, obj =>
                        {
                            _reader.State = this;
                            _curr.Add(obj);
                            _waitForSeperator = true;
                        });
                        _reader.State.Process(c);
                    }
                    else if (c == ',')
                    {
                        _waitForSeperator = false;
                    }
                }
            }

            #endregion
        }

        #endregion


        public static BjSJsonValueKind GetValueKind(object obj)
        {
            if (obj == null)
                return BjSJsonValueKind.Null;
            else if (obj is BjSJsonObject)
                return BjSJsonValueKind.Object;
            else if (obj is BjSJsonArray)
                return BjSJsonValueKind.Array;
            else if (obj is string)
                return BjSJsonValueKind.String;
            else if (obj is decimal)
                return BjSJsonValueKind.Number;
            else if (obj is bool)
                return BjSJsonValueKind.Boolean;
            else
                throw new InvalidDataException("The pased object does not have any Type recognized by BjSJson");
        }

        internal static string GetValueDisplayString(object obj)
        {
            if (obj == null)
                return "null";
            else if (obj is BjSJsonObject)
                return (obj as BjSJsonObject).ToString();
            else if (obj is BjSJsonArray)
                return (obj as BjSJsonArray).ToString();
            else if (obj is string)
                return "\"" + (string)obj + "\"";
            else if (obj is decimal)
                return ((decimal)obj).ToString();
            else if (obj is bool)
                return ((bool)obj).ToString();
            else
                return "Unknown";
        }

        internal static string EscapeString(string value)
        {
            StringBuilder s = new StringBuilder();

            foreach (char c in value)
            {
                switch (c)
                {
                    case '\0': s.Append("\\u0000"); break;
                    case '\\': s.Append("\\\\"); break;
                    case '"': s.Append("\\\""); break;
                    case '\r': s.Append("\\r"); break;
                    case '\n': s.Append("\\n"); break;
                    case '\t': s.Append("\\t"); break;
                    case '\b': s.Append("\\b"); break;
                    case '\f': s.Append("\\f"); break;
                    case '/': s.Append("\\/"); break;
                    default: s.Append(c); break;
                }
            }

            return s.ToString();
        }

        internal static string ToJsonString(object obj, bool compressed, int level)
        {
            if (obj == null)
                return "null";
            else if (obj is BjSJsonObject)
                return (obj as BjSJsonObject).ToJsonString(compressed, level);
            else if (obj is BjSJsonArray)
                return (obj as BjSJsonArray).ToJsonString(compressed, level);
            else if (obj is string)
                return "\"" + BjSJsonHelper.EscapeString((string)obj) + "\"";
            else if (obj is decimal)
                return ((decimal)obj).ToString(System.Globalization.CultureInfo.InvariantCulture);
            else if (obj is bool)
                return (bool)obj ? "true" : "false";
            else
                return "";
        }

        internal static string GetLevelString(int level)
        {
            return new String(' ', level * 4);
        }
    }
}
